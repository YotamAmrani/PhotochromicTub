$13=0
;auto home - enable autohome, flip direction of movement, set speed to 100, set offset(5mm)
$22=1
$23=7
$24=100
$27=5
; Soft limit
$20=1
; Hard limit
$21=0
$130=130
$131=160
$132=100
;G28
;set the system / motors RPM
$100=25
$101=100
$102=25
;set led max value
$30=1000
; set system max speed
$110=9600
$111=1300
$112=9600

; set acceleration rate for x
$120=300
$121=300

G10 P0 L20 X0 Y0 Z0
