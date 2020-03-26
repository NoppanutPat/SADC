/* mbed IBT-2 H-bridge motor controller
 * Copyright (c) 2015, rwunderl, http://mbed.org
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#include "IBT2.h"
#include<string>

IBT2::IBT2(PinName L_pwm, PinName R_pwm, PinName en, float freq):
        _L_pwm(L_pwm), _R_pwm(R_pwm), _en(en) {
    // Set initial conditions
    _period = 1.0f / freq;    // in seconds
    _L_pwm.period(_period);    // same period used for all PwmOuts
    _L_pwm = 0.0;
    _R_pwm.period(_period);
    _R_pwm = 0.0;
    _en = 0;
    _speed = 0.0;
}

void IBT2::setSpeed(float speed) {
    _speed = speed;
    if (_speed > 0.0f) {
        _en = 1;
        // forward
        _L_pwm = _speed*0.95;
        //_R_pwm = 0.0;
        _R_pwm = _speed;
    } else if (_speed < 0.0f) {
        _en = 1;
        // reverse
        // _L_pwm = 0.0;
        _L_pwm = -_speed;
        _R_pwm = -_speed;
    } else /* _speed == 0.0 */ {
        _en = 0;
        _L_pwm = 0.0;
        _R_pwm = 0.0;
    }
}

void IBT2::turnDirection(string direction ,float speed) {
    _speed = speed;
    if (direction == "L"){
        if (_speed > 0.0f) {
            _en = 1;
            // forward
            _L_pwm = _speed;
            _R_pwm = -_speed;
            // _R_pwm = _speed;
        }
    }
    else if (direction == "R"){
        if (_speed > 0.0f) {
            _en = 1;
            // forward
            _L_pwm = -_speed;
            _R_pwm = _speed;
            // _R_pwm = _speed;
        }
    }
    
    
    }

float IBT2::getSpeed(void) {
    return _speed;
}
