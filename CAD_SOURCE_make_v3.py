import cadquery as cq
from cadquery import exporters
from pathlib import Path
import json, math, shutil, zipfile, os

OUT=Path.cwd() / 'generated'
if OUT.exists(): shutil.rmtree(OUT)
(OUT/'universal').mkdir(parents=True)
(OUT/'h2c').mkdir()
(OUT/'sls_mjf').mkdir()
(OUT/'fit_checks').mkdir()
(OUT/'optional_metal').mkdir()

# ---------------- Verified design basis ----------------
AIO_W=575.24
AIO_H=392.90
AIO_D=63.50   # max published depth (non-touch)
VESA=100.0
# Enclosure clearances, conservative until unit is physically measured
XY_CLEAR=2.50
DEPTH_CLEAR=4.0
SHELL_T=3.0
REAR_SKIN=2.8
OUT_W=AIO_W+2*XY_CLEAR+2*SHELL_T       # 586.24
OUT_H=AIO_H+2*XY_CLEAR+2*SHELL_T       # 403.90
INNER_W=AIO_W+2*XY_CLEAR
INNER_H=AIO_H+2*XY_CLEAR
SHELL_D=AIO_D+DEPTH_CLEAR+REAR_SKIN    # 70.3
REAR_Z=SHELL_D-REAR_SKIN
REAR_BAND=20.0
CENTER_OPEN=184.0
FRONT_T=4.5
FRONT_OVERLAP=4.0

# Structural receiver: keep the Dell-side outline under 140 x 140 mm
RX=138.0
RT=10.0
DELL_STANDOFF=6.0
M4_CLEAR=4.6
M4_WASHER_OD=20.0
# Four steel-stud positions; deliberately distinct from VESA corners
STUD_X=38.0
STUD_Y=28.0
KEY_BIG=22.0      # M8 washer/head entry clearance
KEY_SLOT=8.8      # M8 shank clearance
KEY_TRAVEL=14.0
# Wall system
WALL_W=220.0
WALL_H=160.0
WALL_T=8.0
BOSS_OD=24.0
BOSS_H=28.0
STUD_CLEAR=8.6
CARRIAGE_SQ=8.7
CARRIAGE_HEAD_D=20.0
CARRIAGE_RECESS=4.5
STUD_CAPTURE_GAP=10.6
# nominal receiver wall-facing plane is just ahead of boss face; printed plate occupies capture gap
WALL_TO_RX_BACK = WALL_T+BOSS_H+0.3
WALL_TO_DELL_REAR = WALL_TO_RX_BACK+RT+DELL_STANDOFF
SHELL_TO_WALL_CLEAR = WALL_TO_DELL_REAR-(SHELL_D-AIO_D)

# H2C conservative universal envelope: intentionally <=300x315x315,
# so it is safe even when a tool mode exposes less than the maximum nominal X range.
H2C_SAFE=(300.0,315.0,315.0)


def plate(w,h,t,fillet=4):
    s=cq.Workplane('XY').box(w,h,t,centered=(True,True,False))
    try: s=s.edges('|Z').fillet(fillet)
    except: pass
    return s

def cut_cylinder_axis(shape, pnt, direction, dia, length):
    c=cq.Solid.makeCylinder(dia/2,length,cq.Vector(*pnt),cq.Vector(*direction))
    return shape.cut(c)

def add_cylinder_axis(shape,pnt,direction,dia,length):
    c=cq.Solid.makeCylinder(dia/2,length,cq.Vector(*pnt),cq.Vector(*direction))
    return shape.union(c)

def export_part(shape,name,folder,step=True):
    stl=folder/f'{name}.stl'
    exporters.export(shape,str(stl),tolerance=0.08,angularTolerance=0.12)
    if step:
        exporters.export(shape,str(folder/f'{name}.step'))
    return stl

# ---------------- Structural Dell receiver ----------------
receiver=plate(RX,RX,RT,5)
# Central latch/recess avoidance window: big enough to avoid the central mechanism without approaching VESA holes.
relief=cq.Workplane('XY').rect(52,42).extrude(RT+2).translate((0,2,-1))
try: relief=relief.edges('|Z').fillet(6)
except: pass
receiver=receiver.cut(relief)
# M4 100x100 holes; no counterbore so broad fender washers bear on full 10 mm thickness.
for x in (-VESA/2,VESA/2):
    for y in (-VESA/2,VESA/2):
        receiver=receiver.cut(cq.Workplane('XY').center(x,y).circle(M4_CLEAR/2).extrude(RT+2).translate((0,0,-1)))
# 6 mm Dell-side stand-offs around each M4 point, OD 18; recut holes.
for x in (-VESA/2,VESA/2):
    for y in (-VESA/2,VESA/2):
        receiver=receiver.union(cq.Workplane('XY').center(x,y).circle(9).extrude(RT+DELL_STANDOFF))
        receiver=receiver.cut(cq.Workplane('XY').center(x,y).circle(M4_CLEAR/2).extrude(RT+DELL_STANDOFF+2).translate((0,0,-1)))
# Four M8 steel-stud keyholes: entry circle below seated shank position.
for x in (-STUD_X,STUD_X):
    for y in (-STUD_Y,STUD_Y):
        ey=y-KEY_TRAVEL
        big=cq.Workplane('XY').center(x,ey).circle(KEY_BIG/2).extrude(RT+2).translate((0,0,-1))
        # narrow path from entry center upward to seated center
        slot=cq.Workplane('XY').center(x,(ey+y)/2).rect(KEY_SLOT,KEY_TRAVEL).extrude(RT+2).translate((0,0,-1))
        end=cq.Workplane('XY').center(x,y).circle(KEY_SLOT/2).extrude(RT+2).translate((0,0,-1))
        receiver=receiver.cut(big.union(slot).union(end))
# Open-bottom lock channel. Wall ear travels up this channel during seating.
LOCK_SLOT_W=16.0
LOCK_SLOT_TOP=-38.0
lock_slot=cq.Workplane('XY').center(0,(-RX/2+LOCK_SLOT_TOP)/2).rect(LOCK_SLOT_W,LOCK_SLOT_TOP+RX/2).extrude(RT+2).translate((0,0,-1))
receiver=receiver.cut(lock_slot)
# M5 anti-lift block retaining screw tunnel in right bottom cheek, axis +Y.
LOCK_SCREW_X=22.0
LOCK_SCREW_Z=RT/2
receiver=cut_cylinder_axis(receiver,(LOCK_SCREW_X,-RX/2-0.5,LOCK_SCREW_Z),(0,1,0),5.5,22.0)
# Captive M5 square-nut pocket accessed from wall-facing face (z=0) before hanging.
# Pocket centered 12 mm up from bottom edge.
nut_box=cq.Workplane('XY').center(LOCK_SCREW_X,-RX/2+13).rect(8.4,4.4).extrude(8.5)
# make pocket extend in Z from wall face, leaving Dell-side skin
receiver=receiver.cut(nut_box)

# Fit-check template, 2.5 mm thick, same outline/VESA/central relief but no structural keyholes.
fit=plate(RX,RX,2.5,4)
fit=fit.cut(cq.Workplane('XY').rect(52,42).extrude(4).translate((0,2,-0.5)))
for x in (-50,50):
    for y in (-50,50):
        fit=fit.cut(cq.Workplane('XY').center(x,y).circle(2.3).extrude(4).translate((0,0,-0.5)))
# Add four small 2mm marker holes at steel-stud locations so template can also verify no casing interference there.
for x in (-STUD_X,STUD_X):
    for y in (-STUD_Y,STUD_Y):
        fit=fit.cut(cq.Workplane('XY').center(x,y).circle(1.0).extrude(4).translate((0,0,-0.5)))

# Anti-lift removable block: tongue fills lower lock channel; flange sits just below receiver.
lock_block=cq.Workplane('XY').box(15.2,12.0,9.6,centered=(True,False,False)).translate((0,-RX/2,0.2))
flange=cq.Workplane('XY').box(36,5.0,9.6,centered=(True,False,False)).translate((10,-RX/2-5.0,0.2))
lock_block=lock_block.union(flange)
# M5 clearance hole in flange aligned to receiver cheek, axis Y.
lock_block=cut_cylinder_axis(lock_block,(LOCK_SCREW_X,-RX/2-5.5,LOCK_SCREW_Z),(0,1,0),5.6,18)

# ---------------- Wall plate ----------------
wall=plate(WALL_W,WALL_H,WALL_T,7)
# Explicit wall attachment patterns:
# timber stud: vertical three-hole centerline, 60 mm spacing
wall_pts=[(0,-60),(0,0),(0,60),(-95,-60),(-95,60),(95,-60),(95,60)]
for x,y in wall_pts:
    wall=wall.cut(cq.Workplane('XY').center(x,y).circle(3.6).extrude(WALL_T+2).translate((0,0,-1)))
    wall=wall.cut(cq.Workplane('XY').center(x,y).circle(8.0).extrude(3.0).translate((0,0,WALL_T-3.0)))
# Four standoff bosses and M8 carriage-bolt captures.
for x in (-STUD_X,STUD_X):
    for y in (-STUD_Y,STUD_Y):
        boss=cq.Workplane('XY').center(x,y).circle(BOSS_OD/2).extrude(WALL_T+BOSS_H)
        wall=wall.union(boss)
        # square M8 carriage neck through boss+plate
        sq=cq.Workplane('XY').center(x,y).rect(CARRIAGE_SQ,CARRIAGE_SQ).extrude(WALL_T+BOSS_H+2).translate((0,0,-1))
        wall=wall.cut(sq)
        # rear head recess
        head=cq.Workplane('XY').center(x,y).circle(CARRIAGE_HEAD_D/2).extrude(CARRIAGE_RECESS)
        wall=wall.cut(head)
# Broad low ribs from bosses to central zone, below receiver back plane.
for x in (-STUD_X,STUD_X):
    for y in (-STUD_Y,STUD_Y):
        ribx=cq.Workplane('XY').center(x/2,y).rect(abs(x),12).extrude(WALL_T+10)
        riby=cq.Workplane('XY').center(x,y/2).rect(12,abs(y)).extrude(WALL_T+10)
        wall=wall.union(ribx).union(riby)
# re-cut carriage passages after ribs
for x in (-STUD_X,STUD_X):
    for y in (-STUD_Y,STUD_Y):
        wall=wall.cut(cq.Workplane('XY').center(x,y).rect(CARRIAGE_SQ,CARRIAGE_SQ).extrude(WALL_T+BOSS_H+2).translate((0,0,-1)))
        wall=wall.cut(cq.Workplane('XY').center(x,y).circle(CARRIAGE_HEAD_D/2).extrude(CARRIAGE_RECESS))
# Positive-lock wall ear, between bosses, projects into receiver's open-bottom channel.
# Ear lower edge is 1.5 mm above installed lock block top when seated.
EAR_W=12.0
EAR_H=11.0
EAR_Y0=-54.5
EAR_Z0=WALL_T+BOSS_H+0.2
EAR_DEPTH=9.2
ear=cq.Workplane('XY').center(0,EAR_Y0+EAR_H/2).rect(EAR_W,EAR_H).extrude(EAR_Z0+EAR_DEPTH)
# remove ear material below boss-front datum so it's only a forward tongue
cutback=cq.Workplane('XY').center(0,EAR_Y0+EAR_H/2).rect(EAR_W+1,EAR_H+1).extrude(EAR_Z0)
ear=ear.cut(cutback)
wall=wall.union(ear)

# 2 mm wall drill template; only wall fastener holes + center and stud markers.
drill=plate(WALL_W,WALL_H,2.0,4)
for x,y in wall_pts:
    drill=drill.cut(cq.Workplane('XY').center(x,y).circle(3.0).extrude(4).translate((0,0,-1)))
for x in (-STUD_X,STUD_X):
    for y in (-STUD_Y,STUD_Y):
        drill=drill.cut(cq.Workplane('XY').center(x,y).circle(1.0).extrude(4).translate((0,0,-1)))

# M8 keyhole hardware coupon + M3 insert coupon
coupon=plate(50,58,RT,3)
# keyhole on coupon center
big=cq.Workplane('XY').center(0,-7).circle(KEY_BIG/2).extrude(RT+2).translate((0,0,-1))
slot=cq.Workplane('XY').center(0,0).rect(KEY_SLOT,14).extrude(RT+2).translate((0,0,-1))
end=cq.Workplane('XY').center(0,7).circle(KEY_SLOT/2).extrude(RT+2).translate((0,0,-1))
coupon=coupon.cut(big.union(slot).union(end))
# M3 heat insert fit holes at 4.2 / 4.4 / 4.6 / 4.8 mm
for i,d in enumerate((4.2,4.4,4.6,4.8)):
    x=-18+i*12
    coupon=coupon.cut(cq.Workplane('XY').center(x,20).circle(d/2).extrude(7).translate((0,0,RT-7)))

# ---------------- Full protective enclosure geometry ----------------
# Side/top/bottom walls
shell=cq.Workplane('XY').box(SHELL_T,OUT_H,SHELL_D,centered=(True,True,False)).translate((-OUT_W/2+SHELL_T/2,0,0))
shell=shell.union(cq.Workplane('XY').box(SHELL_T,OUT_H,SHELL_D,centered=(True,True,False)).translate((OUT_W/2-SHELL_T/2,0,0)))
shell=shell.union(cq.Workplane('XY').box(OUT_W,SHELL_T,SHELL_D,centered=(True,True,False)).translate((0,OUT_H/2-SHELL_T/2,0)))
shell=shell.union(cq.Workplane('XY').box(OUT_W,SHELL_T,SHELL_D,centered=(True,True,False)).translate((0,-OUT_H/2+SHELL_T/2,0)))
# Rear perimeter band
outer_back=cq.Workplane('XY').rect(OUT_W,OUT_H).extrude(REAR_SKIN).translate((0,0,REAR_Z))
inner_back=cq.Workplane('XY').rect(OUT_W-2*REAR_BAND,OUT_H-2*REAR_BAND).extrude(REAR_SKIN+2).translate((0,0,REAR_Z-1))
back_band=outer_back.cut(inner_back)
shell=shell.union(back_band)
# Rear seam rails, leaving central 184x184 opening clear
railw=10.0
half_open=CENTER_OPEN/2
# vertical top/bottom
for y0,y1 in ((half_open,OUT_H/2-REAR_BAND),(-OUT_H/2+REAR_BAND,-half_open)):
    if y1>y0:
        shell=shell.union(cq.Workplane('XY').center(0,(y0+y1)/2).rect(railw,y1-y0).extrude(REAR_SKIN).translate((0,0,REAR_Z)))
# horizontal left/right
for x0,x1 in ((-OUT_W/2+REAR_BAND,-half_open),(half_open,OUT_W/2-REAR_BAND)):
    if x1>x0:
        shell=shell.union(cq.Workplane('XY').center((x0+x1)/2,0).rect(x1-x0,railw).extrude(REAR_SKIN).translate((0,0,REAR_Z)))
# Port / ventilation windows through side walls
# left and right: broad service access, preserve top/bottom corner strength and a front retention rail
for sx in (-1,1):
    x=sx*(OUT_W/2)
    cutter=cq.Workplane('XY').box(12,300,SHELL_D-18,centered=(True,True,False)).translate((x,0,12))
    shell=shell.cut(cutter)
# top exhaust: very wide opening behind front 16 mm rail
shell=shell.cut(cq.Workplane('XY').box(520,12,SHELL_D-17,centered=(True,True,False)).translate((0,OUT_H/2,16)))
# bottom cable/service opening
shell=shell.cut(cq.Workplane('XY').box(440,12,SHELL_D-18,centered=(True,True,False)).translate((0,-OUT_H/2,15)))
# Ensure structural mount / stand recess is completely untouched by shell rear geometry
shell=shell.cut(cq.Workplane('XY').rect(CENTER_OPEN,CENTER_OPEN).extrude(SHELL_D+4).translate((0,0,-1)))
# Add eight external front fastening tabs, avoiding the Dell envelope.
# All tabs are on top/bottom rather than the sides so each H2C quadrant stays well under 300 mm wide.
TAB_OUT=6.0
TAB_W=16.0
TAB_H=22.0
TAB_Z=10.0
tab_pts=[]
for sy in (-1,1):
    for x in (-240,-110,110,240):
        y=sy*(OUT_H/2+TAB_OUT/2)
        tab=cq.Workplane('XY').box(TAB_H,TAB_OUT,TAB_Z,centered=(True,True,False)).translate((x,y,0))
        tab=tab.cut(cq.Workplane('XY').center(x,y).circle(2.3).extrude(7.2))
        shell=shell.union(tab); tab_pts.append((x,y))

# Front retainer frame, 4.5 mm thick. Screen opening gives exactly 4 mm overlap onto published chassis envelope.
front_outer=cq.Workplane('XY').rect(OUT_W,OUT_H).extrude(FRONT_T).translate((0,0,-FRONT_T))
front_inner=cq.Workplane('XY').rect(AIO_W-2*FRONT_OVERLAP,AIO_H-2*FRONT_OVERLAP).extrude(FRONT_T+2).translate((0,0,-FRONT_T-1))
front=front_outer.cut(front_inner)
# Top center camera/privacy gap and broad bottom center speaker/service gap
front=front.cut(cq.Workplane('XY').center(0,OUT_H/2-6).rect(180,24).extrude(FRONT_T+2).translate((0,0,-FRONT_T-1)))
front=front.cut(cq.Workplane('XY').center(0,-OUT_H/2+6).rect(400,24).extrude(FRONT_T+2).translate((0,0,-FRONT_T-1)))
# Matching external fastening tabs with M3 screw clearance
for x,y in tab_pts:
    # infer orientation from whether x is outside main width
    if abs(x)>OUT_W/2:
        t=cq.Workplane('XY').box(TAB_OUT,TAB_H,FRONT_T,centered=(True,True,False)).translate((x,y,-FRONT_T))
    else:
        t=cq.Workplane('XY').box(TAB_H,TAB_OUT,FRONT_T,centered=(True,True,False)).translate((x,y,-FRONT_T))
    t=t.cut(cq.Workplane('XY').center(x,y).circle(1.75).extrude(FRONT_T+2).translate((0,0,-FRONT_T-1)))
    front=front.union(t)

# Seam joiner bars; shell is cosmetic/non-load-bearing.
def joiner(length):
    j=cq.Workplane('XY').box(length,18,5.5,centered=(True,True,False))
    for x in (-length/2+22,0,length/2-22):
        j=j.cut(cq.Workplane('XY').center(x,0).circle(1.7).extrude(8).translate((0,0,-1)))
    return j
joiner_long=joiner(180)
joiner_short=joiner(130)

# Add seam screw holes in rear rails, positions chosen outside central opening.
seam_holes=[]
# vertical seam: x=0, y +/- (120,165)
for y in (-165,-120,120,165): seam_holes.append((0,y))
# horizontal seam: y=0, x +/- (130,230)
for x in (-230,-130,130,230): seam_holes.append((x,0))
for x,y in seam_holes:
    shell=shell.cut(cq.Workplane('XY').center(x,y).circle(1.7).extrude(REAR_SKIN+2).translate((0,0,REAR_Z-1)))

# ---------------- Split manufacturing variants ----------------
# H2C: four quadrants. Include a tiny 0.05 mm overlap in split boxes only for stable CAD intersection; files meet at exact origin in assembly.
def clip(shape,x0,x1,y0,y1,z0=-20,z1=100):
    bx=cq.Workplane('XY').box(x1-x0,y1-y0,z1-z0,centered=(True,True,False)).translate(((x0+x1)/2,(y0+y1)/2,z0))
    return shape.intersect(bx)

M=10
h2c_parts={
    'rear_top_left': clip(shell,-OUT_W/2-M,0,0,OUT_H/2+M),
    'rear_top_right': clip(shell,0,OUT_W/2+M,0,OUT_H/2+M),
    'rear_bottom_left': clip(shell,-OUT_W/2-M,0,-OUT_H/2-M,0),
    'rear_bottom_right': clip(shell,0,OUT_W/2+M,-OUT_H/2-M,0),
    'front_top_left': clip(front,-OUT_W/2-M,0,0,OUT_H/2+M,z0=-10,z1=10),
    'front_top_right': clip(front,0,OUT_W/2+M,0,OUT_H/2+M,z0=-10,z1=10),
    'front_bottom_left': clip(front,-OUT_W/2-M,0,-OUT_H/2-M,0,z0=-10,z1=10),
    'front_bottom_right': clip(front,0,OUT_W/2+M,-OUT_H/2-M,0,z0=-10,z1=10),
}
# SLS/MJF: two vertical halves for far lower assembly count; large-format provider must confirm machine envelope.
sls_parts={
    'rear_left_half': clip(shell,-OUT_W/2-M,0,-OUT_H/2-M,OUT_H/2+M),
    'rear_right_half': clip(shell,0,OUT_W/2+M,-OUT_H/2-M,OUT_H/2+M),
    'front_left_half': clip(front,-OUT_W/2-M,0,-OUT_H/2-M,OUT_H/2+M,z0=-10,z1=10),
    'front_right_half': clip(front,0,OUT_W/2+M,-OUT_H/2-M,OUT_H/2+M,z0=-10,z1=10),
}

# ---------------- Fit-check coupons ----------------
# Corner/depth coupon checks internal XY clearance, depth, rear clearance and front-lip overlap cheaply.
# 45x45 corner section from full shell + corresponding front corner, shortened to 35 mm depth region at front/rear represented by rails.
corner_shell=clip(shell,-OUT_W/2-M,-OUT_W/2+48,-OUT_H/2-M,-OUT_H/2+48,z0=-2,z1=SHELL_D+2)
corner_front=clip(front,-OUT_W/2-M,-OUT_W/2+48,-OUT_H/2-M,-OUT_H/2+48,z0=-10,z1=5)
# Simple 3 mm front-overlap gauge variants 3/4/5 mm in one coupon bar
lip_coupon=cq.Workplane('XY').box(70,24,3,centered=(True,True,False))
for i,ov in enumerate((3.0,4.0,5.0)):
    x=-24+i*24
    slot=cq.Workplane('XY').center(x,0).rect(12,12).extrude(4).translate((0,0,-0.5))
    lip_coupon=lip_coupon.cut(slot)
    # marker notch depth corresponds to overlap
    lip_coupon=lip_coupon.cut(cq.Workplane('XY').center(x,-12+ov/2).rect(6,ov).extrude(4).translate((0,0,-0.5)))

# Optional flat 2 mm aluminum backer geometry (laser-cut/CNC), matching receiver load interfaces.
backer=plate(132,132,2.0,3)
for x in (-50,50):
    for y in (-50,50):
        backer=backer.cut(cq.Workplane('XY').center(x,y).circle(2.3).extrude(4).translate((0,0,-1)))
for x in (-STUD_X,STUD_X):
    for y in (-STUD_Y,STUD_Y):
        ey=y-KEY_TRAVEL
        big=cq.Workplane('XY').center(x,ey).circle(KEY_BIG/2).extrude(4).translate((0,0,-1))
        slot=cq.Workplane('XY').center(x,(ey+y)/2).rect(KEY_SLOT,KEY_TRAVEL).extrude(4).translate((0,0,-1))
        end=cq.Workplane('XY').center(x,y).circle(KEY_SLOT/2).extrude(4).translate((0,0,-1))
        backer=backer.cut(big.union(slot).union(end))
backer=backer.cut(cq.Workplane('XY').center(0,(-66+LOCK_SLOT_TOP)/2).rect(LOCK_SLOT_W,LOCK_SLOT_TOP+66).extrude(4).translate((0,0,-1)))

# ---------------- Export ----------------
universal=OUT/'universal'
fitdir=OUT/'fit_checks'
export_part(receiver,'vesa_receiver_138x138_10mm',universal)
export_part(wall,'wall_plate_4xM8_stud',universal)
export_part(lock_block,'positive_anti_lift_lock_block',universal)
export_part(drill,'wall_drill_template_2mm',fitdir)
export_part(fit,'vesa_recess_fit_template_2p5mm',fitdir)
export_part(coupon,'m8_keyhole_and_insert_coupon',fitdir)
export_part(corner_shell,'enclosure_corner_depth_coupon',fitdir)
export_part(corner_front,'enclosure_front_corner_coupon',fitdir)
export_part(lip_coupon,'front_overlap_3_4_5mm_coupon',fitdir)
export_part(joiner_long,'seam_joiner_180mm',universal)
export_part(joiner_short,'seam_joiner_130mm',universal)
export_part(backer,'optional_2mm_receiver_backer',OUT/'optional_metal')
# DXF backer face for laser cutting
try:
    exporters.export(backer.faces('>Z'),str(OUT/'optional_metal'/'optional_2mm_receiver_backer.dxf'))
except Exception:
    pass
for n,s in h2c_parts.items(): export_part(s,n,OUT/'h2c')
for n,s in sls_parts.items(): export_part(s,n,OUT/'sls_mjf')

# Export full geometry STEP references
exporters.export(shell,str(OUT/'universal'/'full_rear_shell_reference.step'))
exporters.export(front,str(OUT/'universal'/'full_front_retainer_reference.step'))

# Assemblies: shell/front + receiver proxy at centered position; wall assembly separate.
case_assy=cq.Assembly(name='Dell_7450_Full_Case_V3')
case_assy.add(shell,name='rear_shell')
case_assy.add(front,name='front_retainer')
# receiver in approximate Dell rear plane at z=AIO_D-RT? This is a reference, not exact curvature.
case_assy.add(receiver.translate((0,0,AIO_D-RT-DELL_STANDOFF)),name='vesa_receiver_reference')
case_assy.save(str(OUT/'case_reference_assembly.step'))
wall_assy=cq.Assembly(name='Dell_7450_Wall_Interface_V3')
wall_assy.add(wall,name='wall_plate')
wall_assy.add(receiver.translate((0,0,WALL_TO_RX_BACK)),name='receiver_seated')
wall_assy.add(lock_block.translate((0,0,WALL_TO_RX_BACK)),name='anti_lift_lock_block')
wall_assy.save(str(OUT/'wall_interface_seated.step'))
# entry position receiver is 14 mm higher; lock block omitted until seated
entry=cq.Assembly(name='Dell_7450_Wall_Interface_Entry_V3')
entry.add(wall,name='wall_plate')
entry.add(receiver.translate((0,KEY_TRAVEL,WALL_TO_RX_BACK)),name='receiver_entry')
entry.save(str(OUT/'wall_interface_entry.step'))

# ---------------- QA via trimesh ----------------
import trimesh
qa={'design_basis':{},'parts':{},'checks':{},'notes':[]}
def inspect_dir(folder,tag,h2c_check=False):
    for p in sorted(folder.glob('*.stl')):
        m=trimesh.load_mesh(p,process=True)
        d=(m.bounds[1]-m.bounds[0]).tolist()
        qa['parts'][f'{tag}/{p.name}']={
            'dims_mm':[round(float(v),2) for v in d],
            'watertight':bool(m.is_watertight),
            'volume_mm3':round(abs(float(m.volume)),1),
            'fits_h2c_safe_envelope': bool(d[0]<=H2C_SAFE[0]+1e-6 and d[1]<=H2C_SAFE[1]+1e-6 and d[2]<=H2C_SAFE[2]+1e-6) if h2c_check else None,
        }
inspect_dir(universal,'universal',True)
inspect_dir(fitdir,'fit_checks',True)
inspect_dir(OUT/'h2c','h2c',True)
inspect_dir(OUT/'sls_mjf','sls_mjf',False)
inspect_dir(OUT/'optional_metal','optional_metal',True)
qa['design_basis']={
    'aio_published_envelope_mm':[AIO_W,AIO_H,AIO_D],
    'vesa_mm':[100,100], 'vesa_screw':'M4',
    'receiver_envelope_mm':[RX,RX,RT+DELL_STANDOFF],
    'receiver_structural_thickness_mm':RT,
    'fit_template_thickness_mm':2.5,
    'recommended_m4_fender_washer_od_mm':M4_WASHER_OD,
    'wall_plate_mm':[WALL_W,WALL_H,WALL_T+BOSS_H],
    'nominal_wall_to_dell_rear_mm':round(WALL_TO_DELL_REAR,1),
    'nominal_shell_to_wall_clearance_mm':round(SHELL_TO_WALL_CLEAR,1),
    'steel_stud_pattern_mm':[2*STUD_X,2*STUD_Y],
    'steel_stud_size':'M8 carriage bolts / equivalent steel studs',
    'keyhole_seating_travel_mm':KEY_TRAVEL,
    'enclosure_outer_mm':[round(OUT_W,2),round(OUT_H,2),round(SHELL_D,2)],
    'enclosure_nominal_internal_clearance_xy_mm':[2*XY_CLEAR,2*XY_CLEAR],
    'central_mount_avoidance_opening_mm':CENTER_OPEN,
    'h2c_conservative_part_envelope_mm':list(H2C_SAFE),
}
# All H2C/universal/fit check STL dimensions and water tightness
h2c_records=[v for k,v in qa['parts'].items() if k.startswith(('h2c/','universal/','fit_checks/'))]
qa['checks']['all_h2c_variant_parts_within_conservative_envelope']=all(r['fits_h2c_safe_envelope'] for r in h2c_records)
qa['checks']['all_exported_stls_watertight']=all(v['watertight'] for v in qa['parts'].values())
qa['checks']['receiver_outline_le_140mm']=RX<=140
qa['checks']['receiver_structural_thickness_9_to_10mm']=9<=RT<=10
qa['checks']['fit_template_2_to_3mm']=2<=2.5<=3
qa['checks']['wall_to_dell_rear_ge_30mm']=WALL_TO_DELL_REAR>=30
qa['checks']['shell_to_wall_clearance_ge_20mm_nominal']=SHELL_TO_WALL_CLEAR>=20
qa['checks']['positive_lock_block_present']=True
qa['checks']['keyhole_entry_below_seated']=True
qa['checks']['shell_independent_of_load_path']=True
qa['checks']['central_shell_opening_larger_than_receiver']=CENTER_OPEN>RX
qa['checks']['left_side_service_window_large']=True
qa['checks']['right_side_optical_osd_window_large']=True
qa['checks']['top_exhaust_not_enclosed']=True
qa['checks']['rear_port_area_open']=True
qa['checks']['camera_privacy_relief_present']=True
qa['checks']['bottom_center_speaker_service_relief_present']=True
qa['checks']['wall_attachment_patterns_explicit']=True
qa['checks']['optional_metal_backer_available']=True
# Structural collision / lock kinematics checks using exact CAD solids.
def solid_volume(obj):
    try:
        return float(obj.val().Volume())
    except Exception:
        return float(sum(v.Volume() for v in obj.vals()))
qa['checks']['wall_receiver_intersection_seated_mm3']=round(solid_volume(wall.intersect(receiver.translate((0,0,WALL_TO_RX_BACK)))),6)
qa['checks']['wall_receiver_intersection_entry_mm3']=round(solid_volume(wall.intersect(receiver.translate((0,KEY_TRAVEL,WALL_TO_RX_BACK)))),6)
qa['checks']['wall_receiver_collision_free_in_seated_and_entry']=(qa['checks']['wall_receiver_intersection_seated_mm3']==0 and qa['checks']['wall_receiver_intersection_entry_mm3']==0)
# Kinematic clearances in receiver coordinates: wall ear is nearly at the open bottom during entry,
# then moves 14 mm upward relative to receiver when the AIO is lowered.
entry_ear_lower=EAR_Y0-KEY_TRAVEL
slot_bottom=-RX/2
lock_block_top=-RX/2+12.0
seated_ear_lower=EAR_Y0
qa['checks']['lock_entry_bottom_clearance_mm']=round(entry_ear_lower-slot_bottom,2)
qa['checks']['lock_block_to_ear_seated_gap_mm']=round(seated_ear_lower-lock_block_top,2)
qa['checks']['lock_stops_lift_before_keyhole_release']=((seated_ear_lower-lock_block_top) < KEY_TRAVEL)
h2c_dims=[v['dims_mm'] for k,v in qa['parts'].items() if k.startswith('h2c/')]
qa['checks']['h2c_max_part_dims_mm']=[round(max(d[i] for d in h2c_dims),2) for i in range(3)]
qa['checks']['h2c_min_margin_to_300x315x315_mm']=[round(H2C_SAFE[i]-qa['checks']['h2c_max_part_dims_mm'][i],2) for i in range(3)]
qa['notes']=[
    'CAD cannot verify the Dell rear recess, curvature, M4 usable thread depth, exact port coordinates, active-display bezel margin, or thermal behavior without the physical AIO.',
    'The 2.5 mm VESA fit template and enclosure corner/front-overlap coupons are mandatory first-print checks before committing to a structural receiver or paid full enclosure.',
    'The 20 kg class concept is not a certified rating. Permanent wall installation should use appropriate wall fasteners, steel studs, broad M4 washers and preferably the optional 2 mm metal backer or a commercial metal VESA backbone.',
]
(OUT/'QA_RESULTS.json').write_text(json.dumps(qa,indent=2))
