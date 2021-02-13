from manim import *
import numpy as np

class IncidentLaser(ThreeDScene):

    def construct(self):
        #Axes to help while developing
        axes = ThreeDAxes()

        #Make and place the mirror
        mirror = Prism([2,0.1,2], fill_opacity=1)
        mirrorY = 2.5
        mirrorPosition = np.array([0,mirrorY,0])
        mirror.set_y(mirrorY)
        mirrorLabel = TextMobject("Mirror")
        mirrorLabel.rotate_in_place(TAU/2)
        mirrorLabel.shift(3*UP)
        
        #Build Laser
        beamColor = RED_E
        laserRadius = 0.2
        laserHeight = 2
        laser = Cylinder(
            radius = laserRadius,
            height = laserHeight,
            fill_opacity=0.85,
            fill_color=GREY,
            checkerboard_colors=[GREY, GREY]
        )
        glow = Circle(
            radius=laserRadius / 5.0,
            shade_in_3d=True,
            fill_color=beamColor
        )
        glow.shift(laserHeight * OUT / 2.0)
        laser.add(glow)
        laserLabel = TextMobject("Laser")
        laserLabel.rotate_in_place(3*TAU/8)
        laserLabel.shift(4.7*RIGHT + 3*DOWN)

        #Place Laser so it is points at 45 deg to mirror
        laser.rotate(-TAU/4.0, axis=RIGHT)
        laser.rotate(-7.0 * TAU / 8.0, axis=OUT)
        laser.shift( 5.0*RIGHT + 2.5*DOWN)

        #Create Incident Laser Beam
        
        x0 = 5-laserHeight*np.sqrt(2)/4
        y0 = -x0 + mirrorY
        incidentBeam = Line([x0, y0,0], [0,mirrorY,0], color=beamColor)
        # self.add(incidentBeam)

        #Create Reflected Laser Beam
        xf = -7
        yf = xf + 2.5
        reflectedBeam = Line([0,mirrorY,0], [xf, yf, 0], color=beamColor)
        # self.add(reflectedBeam)

        #Create S E-Field
        λ = 1
        sColor = TEAL
        sIncidentField = ParametricFunction(
            lambda t: [t, -t+mirrorY,  np.sin(2*PI/λ * t)],
            t_min = 0,
            t_max = x0,
            color = sColor   
        )
        sReflectedField = ParametricFunction(
            lambda t: [t, t+mirrorY,  np.sin(2*PI/λ * t)],
            t_min = xf,
            t_max = 0,
            color = sColor
        )

        # self.add(sIncidentField, sReflectedField)

        #Create P E-Field
        # Because this is is being created on the x-axis and then rotated the
        # units in x are not the same as t. In fact, they are 1/sqrt(2) times
        # shorter. Thus the wavelength looks shorters. Multiplying by sqrt(2)
        # compensates for that. 
        λ = 1 * np.sqrt(2)
        pColor = PURPLE_A
        sColor = TEAL_D
        θ = 7.0 * TAU / 8.0
        rotation = np.array([
                            [np.cos(θ), -np.sin(θ), 0],
                            [np.sin(θ), np.cos(θ), 0 ],
                            [0,0,0]
                            ]
                        )
        
        pIncidentField = ParametricFunction(
            lambda t: rotation.dot(np.array([[t], [np.sin(2*PI/λ * t)], [0]])).flatten()+[0,mirrorY,0],
            t_min = 0,
            t_max = x0 * np.sqrt(2),
            color = pColor   
        )

        θ = 1.0 * TAU / 8.0
        rotation = np.array([
                            [np.cos(θ), -np.sin(θ), 0],
                            [np.sin(θ), np.cos(θ), 0 ],
                            [0,0,0]
                            ]
                        )

        pReflectedField = ParametricFunction(
            lambda t: rotation.dot(np.array([[t], [np.sin(2*PI/λ * t)], [0]])).flatten() + mirrorY*UP,
            t_min = xf * np.sqrt(2),
            t_max = 0,
            color = pColor
        )

        # self.add(pIncidentField, pReflectedField)

        #Normal Vector
        normal = Arrow(mirrorPosition+0.2*UP, mirrorPosition+4*DOWN, color=BLUE_D)
        normalLabel = TexMobject(r"\vec{\mathbf{N}}", color=BLUE_D).scale(1.5)
        normalLabel.rotate_in_place(TAU/2)
        normalLabel.shift(2 * DOWN)
        # self.add(normalLabel)

        # Law of Reflection
        arc1 = Sector(
                    outer_radius=2, 
                    start_angle=-TAU/8, 
                    angle=-TAU/8, 
                    fill_color=RED_A,
                    stroke_width=8,
                    fill_opacity = 0.9,
                    stroke_color=RED_B,
                    arc_center=mirrorPosition
                )
        
        arc2 = Sector(
                    outer_radius=2, 
                    start_angle=-TAU/4, 
                    angle=-TAU/8, 
                    fill_color=YELLOW_A,
                    stroke_width=8,
                    fill_opacity = 0.9,
                    stroke_color=YELLOW_B,
                    arc_center=mirrorPosition
                )
        
        θi1 = TexMobject(r"\theta_i", color=RED_B).scale(1.5)
        θi1.shift(1*RIGHT)
        θi1.rotate_in_place(TAU/2)

        θi2 = TexMobject(r"\theta_i", color=RED_B).scale(1.5)
        θi2.shift(0.5*RIGHT + 3*DOWN)
        θi2.rotate_in_place(TAU/2)
        # self.add(θi1, θi2)

        θr1 = TexMobject(r"\theta_r", color=YELLOW_B).scale(1.5)
        θr1.shift(-1*RIGHT)
        θr1.rotate_in_place(TAU/2)

        θr2 = TexMobject(r"\theta_r", color=YELLOW_B).scale(1.5)
        θr2.shift(-0.6*RIGHT + 3*DOWN)
        θr2.rotate_in_place(TAU/2)

        equals = TexMobject(r"=")
        equals.rotate_in_place(TAU/2)
        equals.shift(3*DOWN)
        # self.add(θr1, θr2, equals)
        
        #Z Vector
        unitLength = 0.65
        η = 0.17
        tipLength = η*unitLength
        lineLength = unitLength - tipLength
        
        zLength = 0.35
        zi = Line([x0-1, y0+1, 0], [x0-1-lineLength, y0+1+lineLength, 0], color=YELLOW).add_tip(tip_length=tipLength)
        ziLabel = TexMobject(r"\hat{\mathbf{z}}", color=YELLOW)
        ziLabel.rotate_in_place(TAU/2)
        ziLabel.shift(0.25*DOWN + 0.95*(x0-1)*RIGHT)
        ziGroup = VGroup()
        ziGroup.add(zi, ziLabel)

        #E Vector
        offset = 0.25
        eLength=0.35
        # E = Arrow([x0, y0, 0], [x0-eLength, y0+eLength, 0], color=GREEN_SCREEN)
        # E.rotate(TAU/4, axis=-LEFT+UP, about_point=[x0,y0,0])
        # E.shift(offset*IN)
        tLength = 0.15*eLength
        E = Line([x0,y0,0], [x0-lineLength, y0+lineLength, 0], color=GREEN_SCREEN).add_tip(tip_length=tLength)
        E.rotate(TAU/4, axis=-LEFT+UP, about_point=[x0,y0,0])
        eLabel = TexMobject(r"\hat{\mathbf{E}}", color=GREEN_SCREEN)
        eLabel.rotate(TAU/2).rotate(TAU/4, axis=LEFT).rotate(5*TAU/8)
        eLabel.shift([x0+0.25, y0+0.25, -0.35])
        eLabel.scale(0.5)
        
        # p = Line(ORIGIN, [-unitLength, 0, 0], color=PURPLE_A).add_tip(tip_length=tLength)
        # s = Line(ORIGIN, [0, -unitLength, 0], color=TEAL_D).add_tip(tip_length=tLength)
        
        p = Arrow2(ORIGIN, length=unitLength, theta=TAU/2, color=pColor)
        s = Arrow2(ORIGIN, length=unitLength, theta=3*TAU/4, color=sColor)
        pLabel = MathTex(r"\hat{\mathbf{p}}", color=pColor)
        sLabel = MathTex(r"\hat{\mathbf{s}}", color=sColor)
        pLabel.rotate(TAU/2).shift(0.25*(LEFT+UP)).scale(0.5)
        sLabel.rotate(TAU/2).shift(0.25*(LEFT+DOWN)).scale(0.5)

        pGroup = VGroup().add(p, pLabel)
        sGroup = VGroup().add(s, sLabel)
        spGroup = VGroup().add(sGroup, pGroup)

        

        m1Vector = Arrow2(mirrorPosition, theta=7*TAU/8)
        m2Vector = Arrow2(mirrorPosition, theta=5*TAU/8)



        numberPlane = NumberPlane().scale(0.2).set_opacity(0)
        planeFill = 0.1
        planeColor = WHITE
        plane = Rectangle(
            width=numberPlane.get_width(), 
            height=numberPlane.get_height(),
            fill_color=planeColor,
            fill_opacity=planeFill
        )


        plane.rotate_in_place(TAU/2, axis=UP)
        circleTrace = Circle(
            radius=unitLength+tipLength,
            fill_opacity=planeFill,
            color=planeColor,
            stroke_width=5,
            stroke_color=planeColor
        )

        planePosition0 = np.array([x0,y0,0])
        planes = VGroup().add(plane, numberPlane, circleTrace)
        planes.rotate(TAU/4, axis=LEFT)
        planes.rotate(TAU/8)
        planes.shift(planePosition0)

        spGroup.rotate(TAU/4, axis=LEFT, about_point=s.get_start()).rotate(TAU/8, about_point=s.get_start()).shift(planePosition0)

        tempDot = Dot(planePosition0, radius=0.04, color=beamColor)
        tempDot.rotate(TAU/4, axis=LEFT+DOWN, about_point=planePosition0)

        pplane = Rectangle(
            width=2.75, 
            height=1.60,
            fill_color=planeColor,
            fill_opacity=planeFill
        )
        pplane.rotate(TAU/4, axis=LEFT)
        pplane.shift(mirrorPosition)

        planeDot = Dot(mirrorPosition+1.6/2*OUT, radius=0.08, color=TEAL_D)
        planeLine = Line(mirrorPosition+3*IN, mirrorPosition+3*OUT)

        basicGroup = VGroup()
        basicGroup.add(
            normal,
            normalLabel, 
            laser, 
            laserLabel, 
            mirror, 
            mirrorLabel, 
            incidentBeam,
            reflectedBeam)
        
        eFieldGroup1 = VGroup()
        eFieldGroup1.add(
            sIncidentField,
            E
        )

    
        #Animations
        # self.set_camera_orientation(phi=0 * DEGREES, theta=90 * DEGREES)
        # self.play(
        #     ShowCreation(laser),
        #     Write(laserLabel),
        #     runtime=2
        # )
        # self.wait()
        # self.play(
        #     ShowCreation(mirror),
        #     Write(mirrorLabel),
        #     runtime=2
        # )
        # self.wait(2)
        # self.play(ShowCreation(incidentBeam), runtime=3)
        # self.play(ShowCreation(reflectedBeam), runtime=3)
        # # self.stop_ambient_camera_rotation()
        # # self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES)
        # self.wait()
        # self.play(ShowCreation(normal))
        # self.play(ShowCreation(normalLabel))

        # self.play(ShowCreation(arc1), ShowCreation(arc2), runtime=2)
        # self.play(ShowCreation(θi1), ShowCreation(θr1))
        # self.play(WiggleOutThenIn(θi1), WiggleOutThenIn(arc1))
        # self.play(WiggleOutThenIn(θr1), WiggleOutThenIn(arc2))
        # self.play(
        #     ReplacementTransform(θi1,θi2),
        #     ReplacementTransform(θr1, θr2)
        # )
        # self.add(equals)
        # self.wait()
        # self.play(
        #     FadeOut(θi2),
        #     FadeOut(θr2),
        #     FadeOut(arc1),
        #     FadeOut(arc2),
        #     FadeOut(equals),
        #     runtime = 2
        # )

        # ziGroup2 = ziGroup.copy()
        # self.play(ShowCreation(ziGroup2))
        # self.play(WiggleOutThenIn(ziGroup2))
        # self.play(
        #     ApplyMethod(ziGroup2.shift, mirrorPosition-ziGroup2[0].get_start())
        # )

        # ziGroup2[0].rotate(TAU/4, about_point=mirrorPosition)
        # self.play(
        #     ApplyMethod(ziGroup2.shift, np.array([xf+2, yf+2, 0])-ziGroup2[0].get_start() )
        # )
        # self.play(
        #     FadeOut(ziGroup2),
        #     FadeIn(ziGroup),
        #     runtime=2
        # )
        # self.add(laser, laserLabel, mirror, mirrorLabel, incidentBeam, reflectedBeam, normal)
        # self.add(ziGroup)
        # self.wait(2)

        # self.move_camera(phi=TAU/8, theta=TAU*(1/4+1/10), runtime=3)
        # self.begin_ambient_camera_rotation(rate= TAU*(5/8-1/10) * 1/8)
        # self.wait(8)
        # self.stop_ambient_camera_rotation()

        # self.move_camera(phi=TAU/5)
        # tempAngle = TAU/12
        # sIncidentField.rotate(tempAngle, axis=UP+LEFT, about_point=mirrorPosition)
        # E.rotate(tempAngle, axis=UP+LEFT, about_point=mirrorPosition)
        # self.play(
        #     ShowCreation(sIncidentField),
        #     FadeOut(ziGroup),
        #     runtime=2
        # )
        # tempAngle += -TAU/3
        # self.play(Rotate(sIncidentField, angle=tempAngle, axis=UP+LEFT, about_point=mirrorPosition))
        # E.rotate(angle=tempAngle, axis=UP+LEFT, about_point=mirrorPosition)
        # self.wait()
        # tempAngle += TAU/2.5
        # self.play(Rotate(sIncidentField, angle=tempAngle, axis=UP+LEFT, about_point=mirrorPosition))
        # E.rotate(angle=tempAngle, axis=UP+LEFT, about_point=mirrorPosition)
        # self.wait()
        # tempAngle += TAU/8
        # self.play(Rotate(sIncidentField, angle=tempAngle, axis=UP+LEFT, about_point=mirrorPosition))
        # E.rotate(angle=tempAngle, axis=UP+LEFT, about_point=mirrorPosition)




        self.move_camera(phi=TAU/4, theta=7*TAU/8, frame_center=mirrorPosition, distance=12)
        self.play(
            FadeOut(basicGroup),
            FadeIn(tempDot)
        )
        self.play(
            ShowCreation(E),
            Write(eLabel)
            # ApplyMethod(tempDot.shift, 0.2*IN)
        )

        self.play(Indicate(E))
        self.play(Indicate(eLabel))
        self.play(FadeOut(eLabel))

        tempAngle = TAU/3
        self.play(Rotate(eFieldGroup1, angle=tempAngle, axis=UP+LEFT, about_point=mirrorPosition))
        self.wait(0.25)
        tempAngle -= TAU/5
        self.play(Rotate(eFieldGroup1, angle=tempAngle, axis=UP+LEFT, about_point=mirrorPosition))
        self.wait(0.25)
        tempAngle -= TAU/1.2
        self.play(
            Rotate(eFieldGroup1, angle=tempAngle, axis=UP+LEFT, about_point=mirrorPosition),  
        )
        self.wait(0.25)
        self.play(FadeOut(sIncidentField))
        tempAngle += TAU/3.4
        self.play(Rotate(E, angle=tempAngle, axis=UP+LEFT, about_point=mirrorPosition))
        sIncidentField.rotate(angle=tempAngle, axis=UP+LEFT, about_point=mirrorPosition)
        self.wait(0.25)
        tempAngle += TAU/12
        self.play(Rotate(E, angle=tempAngle, axis=UP+LEFT, about_point=mirrorPosition))
        sIncidentField.rotate(angle=tempAngle, axis=UP+LEFT, about_point=mirrorPosition)
        self.wait(0.25)
        tempAngle += TAU/2.2
        self.play(Rotate(E, angle=tempAngle, axis=UP+LEFT, about_point=mirrorPosition))
        sIncidentField.rotate(angle=tempAngle, axis=UP+LEFT, about_point=mirrorPosition)
        circleTrace.rotate(
            -angle_between(RIGHT+UP, E.get_unit_vector()), 
            axis=LEFT+UP,
            about_point=mirrorPosition
        )
        self.play(
            Rotate(E, angle=TAU-0.001, axis=UP+LEFT, about_point=mirrorPosition),
            ShowCreation(circleTrace)
        )
        # plane.rotate_in_place(TAU/2)
        # circleTrace.rotate_in_place(TAU/2, axis=OUT)
        self.play(
            FadeIn(basicGroup+ziGroup),
            FadeOut(tempDot),
            Transform(circleTrace, plane)
        )
        self.move_camera(phi=TAU/5, theta=7*TAU/8, frame_center=ORIGIN, distance = 20)
        self.begin_ambient_camera_rotation(rate=TAU/20)
        self.play(
            ApplyMethod((planes).shift, LEFT+UP),
            ApplyMethod(E.shift, LEFT+UP)
        )
        spGroup.shift(LEFT+UP)
        
        self.wait(5)
        # self.stop_ambient_camera_rotation()
        # camGap = 4
        # m = -1
        # q = -np.sqrt( camGap**2 / (m**2 + 1) )
        planePosition = np.array([x0-1, y0+1, 0])
        # theta = np.arctan( (planePosition[1] + m*q) / (planePosition[0] + q) )
        # r = (planePosition[0] + q) / np.cos(theta)
        # print(f"X,Y = {planePosition[0]},{planePosition[1]}")
        # print("R:",r)
        # print("Th:", theta)
        # print()
        # # normalVect = planePosition - np.array([x0,y0,0])
        # # r = planePosition + camGap*normalVect
        # # rMag = np.sqrt( r[0]**2 + r[1]**2 + r[2]**2 )
        # # self.add(axes)
        # position = [r*np.cos(theta), r*np.sin(theta), 0]
        # d = Dot(position)
        # self.add(d)
        # self.move_camera(phi=TAU/4+0.001, theta=theta, distance=r, frame_center=ORIGIN)
        # self.wait()
        # self.remove(d)
        # self.wait()
        # self.add(d)
        # self.wait()
        # self.remove(d)
        # self.wait()
        # self.add(d)
        # self.play(
        #     FadeOut(basicGroup),
        #     FadeIn(tempDot)
        # )
        # tempDot.move_to([x0-1, y0+1, 0])
        # self.wait()
        # self.move_camera(frame_center=planePosition)
        # self.wait()
        # self.move_camera(theta=3*TAU/8+0.001)
        # self.wait()
        # self.move_camera(frame_center=[x0+8, y0-8, 0 ])
        # self.wait()
        # self.move_camera(distance=20)
        # self.wait()
        # self.move_camera(frame_center=[x0-4, y0+4, 0 ])
        # self.wait()
        # self.move_camera(frame_center=[x0-3, y0+3, 0 ])
        # self.wait()
        # self.move_camera(frame_center=[x0-2, y0+2, 0 ])
        # self.wait()
        # self.move_camera(distance=15)
        # self.wait()
        # self.move_camera(distance=10)
        # self.wait()
        # self.move_camera(distance=5)
    
        # self.move_camera(phi=0, theta=TAU/4, distance=10, frame_center=planePosition)
        
        
        self.wait(3)
        self.stop_ambient_camera_rotation()
        self.wait()
        # REMEMBER TO COUNT THE ROTATIONS YOU"VE ALREADY MADE. i.e. ADD TAU!
        self.move_camera(phi=TAU/4, theta=3*TAU/8+TAU, frame_center=mirrorPosition, distance=30)
        self.play(
            FadeOut(basicGroup),
            FadeIn(tempDot)
        )
        tempGroup = planes+tempDot+E
        tempGroup.save_state()
        spGroup.save_state()
        self.play(ApplyMethod((tempGroup).scale_in_place, 4))
        spGroup.scale_about_point(4, s.get_start())
        self.wait()
        numberPlane.set_opacity(1)
        self.play(FadeIn(numberPlane))
        totalAngle = 0
        for i in range(3):
            angle = np.random.uniform(-TAU, TAU)
            totalAngle += angle
            self.play(Rotate((planes), angle, axis=LEFT+UP))
            spGroup.rotate(angle, axis=LEFT+UP, about_point=s.get_start())
            self.wait()

        self.play( ShowCreation(s) )
        self.wait(0.3)
        self.play( ShowCreation(p) )

        self.play( Rotate(planes+s+p, -totalAngle, axis=LEFT+UP, about_point=mirrorPosition) )
        self.play(
            ApplyMethod(tempGroup.restore),
            FadeOut(s),
            FadeOut(p)
        )
        spGroup.restore()
        # self.move_camera(phi=0, theta=TAU/4, frame_center=ORIGIN)
        self.camera.reset()
        newFrameCenter = mirrorPosition+1.35*DOWN
        self.move_camera(phi=0, theta=TAU/4 + TAU, frame_center=newFrameCenter)
        self.play(
            FadeIn(basicGroup),
            FadeOut(E)
        )
        self.remove(ziGroup)
        self.add(ziGroup)
        self.move_camera(phi=TAU/8, theta=TAU+5*TAU/8)
        self.play(
            FadeIn(pplane),
            FadeOut(mirror),
            FadeOut(mirrorLabel)
        )
        self.wait()
        delta = mirrorPosition - planePosition
        self.play(ApplyMethod((ziGroup+planes).shift, delta, runtime=2))
        spGroup.shift(delta)
        self.wait()
        self.move_camera(phi=0, frame_center=mirrorPosition)
        self.play( ShowCreation(planeDot) )
        self.wait()
        self.play(WiggleOutThenIn(planeDot))
   
        self.move_camera(phi=TAU/5, run_time=2)
        self.wait()
        self.play( ShowCreation(planeLine) )
        self.move_camera(phi=TAU/5, theta=3*TAU/8+TAU+0.2, frame_center=mirrorPosition, run_time=8)
        self.wait()
        tempGroup = VGroup().add(planes, pplane, planeDot, planeLine, ziGroup)
        tempGroup1 = tempGroup-planeDot-planeLine-pplane
        tempGroup1.save_state()
        spGroup.save_state()
        self.play(
            FadeOut(basicGroup-mirror-mirrorLabel),
            ApplyMethod((tempGroup).scale, 4)
        )
        spGroup.scale_about_point(4, s.get_start())
        self.play( ShowCreation(s) )
        self.wait()
        self.play(
            FadeOut(pplane),
            FadeOut(planeDot),
            FadeOut(planeLine)
        )
        self.wait()
        self.play( FadeIn(sLabel) )
        self.wait()
        self.play( FadeIn(numberPlane))
        self.wait()
        self.play(Indicate(sGroup))
        self.wait()
        self.play(Indicate(ziGroup))
        self.wait()
        self.play(ShowCreation(p))
        self.wait()
        self.play(ShowCreation(pLabel))
        self.wait()
        self.play(
            ApplyMethod(tempGroup1.restore),
            ApplyMethod(spGroup.restore),
        )
        self.play( 
            FadeIn(basicGroup),
            FadeOut(planes+ziGroup),
            )
        self.wait()
        self.move_camera(phi=0, theta=TAU+TAU/4, frame_center=newFrameCenter)
        self.wait()
        self.play(ShowCreation(m1Vector))
        self.wait()
        self.play(ShowCreation(m2Vector))
        self.move_camera(phi=TAU/8, theta=TAU+TAU/8, run_time=2)
        self.begin_ambient_camera_rotation(rate=-TAU/20)
        self.wait(1)
        self.play(Rotate(m2Vector, TAU/4), run_time=2)
        self.play(Rotate(m2Vector, -TAU/4), run_time=2)




      








        # Quick Test
        # self.add(laser, laserLabel, mirror, mirrorLabel, incidentBeam, reflectedBeam, normal)
        # self.add(ziGroup)
        # self.add(axes)
        # self.add(laser, E)
        # self.begin_ambient_camera_rotation(1)
        # self.play(Rotate(E, TAU/4, axis=-LEFT+UP, about_point=[x0,y0,0]))
        # self.wait(5)
        # p = NumberPlane().add_background_rectangle(color=WHITE, opacity=0.3)
        # self.add(p)
        # self.play(Rotate(p, TAU/12))
        # self.wait()



#############################
##      Object Classes     ##
#############################

class SectorTrace(Scene):

    def construct(self):

        circ = Circle(
            fill_opacity=0.3,
            stroke_color=WHITE,
            stroke_width=6,
            color=WHITE
        )
        
        rect = Rectangle(
            width=3,
            height=5,
            fill_opacity=0.3,
            color = WHITE,
            stroke_width=3,
            stroke_color=WHITE
        )
        rect.rotate(TAU/2, axis=UP)
        rect.rotate(TAU/4)
        circ.rotate(TAU/4)
        unitLength = 1
        η = 0.17
        tipLength = η*unitLength
        lineLength = unitLength - tipLength
        vect = Line(ORIGIN, [0, unitLength, 0]).add_tip(tip_length=tipLength)
        trace = TracedPath(vect.get_end).suspend_updating()
        self.add(vect, trace, Dot(ORIGIN))
        self.wait()
        def updater(arc):
            arc.angle = angle_between(UP, vect.get_unit_vector()
            )
        
        self.play(
            Rotate(vect, TAU-0.001, about_point=ORIGIN, run_time=4),
            ShowCreation(circ, run_time=4)
        )
        self.play(
            Transform(circ, rect)
        )
        self.wait()


class Cylinder(VGroup):

    def __init__(self, 
        radius=1, 
        height=2,
        resolution=(12,24),
        u_min = 0,
        u_max = TAU,
        v_min = -1,
        v_max = 1,
        fill_opacity = 0.75,
        fill_color = BLUE,
        stroke_width=0,
        **kwargs
    ):
        self.radius = radius
        self.height = height
        if height != 2:
            v_max = height/2
            v_min = -height/2
        
        super().__init__(
            fill_color=fill_color,
            fill_opacity=fill_opacity,
            stroke_width=stroke_width,
            **kwargs
        )
        self.walls = ParametricSurface(
            self.func,
            resolution=resolution,
            u_min=u_min,
            u_max=u_max,
            v_min=v_min,
            v_max=v_max,
            **kwargs
        )

        # self.top = Circle()
        # self.top.set_fill(fill_color)
        # self.top.set_z(self.height/2)
        # self.bottom = Circle()
        # self.bottom.set_fill(fill_color)
        # self.bottom.set_z( -self.height/2)
        # self.bottom.flip()
        # # self.add(self.bottom, self.top, self.walls)
        self.add(self.walls)

    def generate_points(self):
        for vect in IN, OUT:
            face = Circle(
                radius=self.radius,
                shade_in_3d=True
            )
            face.flip()
            face.shift(self.height * OUT / 2.0)
            face.apply_matrix(z_to_vector(vect))
            self.add(face)

    def func(
        self, u, v
    ):
        return np.array([self.radius*np.cos(u), self.radius*np.sin(u), v])

class Arrow2(Line):

    def __init__(self, position, length=1, theta=0, phi=TAU/4, tipRatio=0.15, **kwargs):
        self.position = np.array(position)
        self.length = length
        self.theta = theta
        self.phi = phi
        self.tipRatio = tipRatio
        self.lineLength = (1-tipRatio) * length
        end = length * np.array( [np.sin(phi)*np.cos(theta), np.sin(phi)*np.sin(theta), np.cos(phi)] )
        end = self.position + end
        print(position, end)
        super().__init__(
            start=self.position,
            end=end,
            **kwargs
        )
        self.add_tip(tip_length=tipRatio*length)

    
    def rotate(self, angle, axis=OUT, about_point=ORIGIN, **kwargs):
        rot_matrix = rotation_matrix(angle, axis)
        self.apply_points_function_about_point(
            lambda points: np.dot(points, rot_matrix.T), 
            about_point=self.get_start(),
            **kwargs
        )
        return self

    def scale(self, scale_factor, about_point=ORIGIN, **kwargs):
        self.apply_points_function_about_point(
            lambda points: scale_factor * points, **kwargs,
            about_point=self.get_start()
        )
        return self
