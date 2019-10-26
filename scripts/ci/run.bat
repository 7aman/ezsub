@echo off
REM yes n | ezsub update
REM ezsub login
ezsub cfg set Defaults.group True
ezsub cfg set Defaults.auto_select True
ezsub cfg set Defaults.open_after False
ezsub cfg set Defaults.site subscene hastisub subf2m xyz
ezsub cfg set Defaults.lngs en fa
ezsub clean -t wilderpeople
ezsub dl -t wilderpeople
ezsub x -t wilderpeople
ezsub history run 2
ezsub info
ezsub backup -O
ezsub clean -t wilderpeople -l en --zero
ezsub clean -t wilderpeople
ezsub cfg show
ezsub h show
ezsub cfg set Defaults.group True
ezsub cfg set Defaults.auto_select False
ezsub cfg set Defaults.open_after True
ezsub cfg set Defaults.site hastisub subf2m xyz
ezsub cfg set Defaults.lngs en fa