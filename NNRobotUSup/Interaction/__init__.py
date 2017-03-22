#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Record as r
import Watson as w
import TextToSpeak as txtsp
import Speak as Speak

speak = Speak.Speak()
textSpeak = txtsp.TextToSpeak()
watson = w.Watson()
resp = watson.talk("busca un niño")
print resp[0]
out = textSpeak.generateSpeak(resp[0])
speak.speak(out)
#rec=r.Record()
#rec.record()
