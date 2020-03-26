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

#ifndef MBED_IBT2_H
#define MBED_IBT2_H

#include "mbed.h"
#include<string>
 
/** Interface to the IBT-2 H-bridge motor controller
 *
 * Control a DC motor connected to the IBT-2 H-bridge using one of two modes:
 *
 * Mode 1:
 *     2 PwmOuts and 1 DigitalOut
 *     - L_PWM controlled with a PwmOut
 *     - R_PWM controlled with a PwmOut
 *     - L_EN, R_EN connected to a DigitalOut (High is Enabled)
 *
 * Mode 2:
 *     1 PwmOut and 2 DigitalOuts
 *     - L_PWM connected to a DigitalOut (High is Forward; keep R_PWM Low)
 *     - R_PWM connected to a DigitalOut (High is Reverse; keep L_PWM Low)
 *     - L_EN, R_EN controlled with a PwmOut
 *
 * For now, only Mode 1 is used.
 */
class IBT2 {
public:
    /** Create an IBT-2 control interface    
     *
     * @param L_pwm A PwmOut pin, driving the L_PWM H-bridge line to control the forward speed.
     * @param R_pwm A PwmOut pin, driving the R_PWM H-bridge line to control the reverse speed.
     * @param en A DigitalOut pin, driving the L_EN and R_EN H-bridge enable lines.
     * @param freq The frequency of the H-bridge PWM lines in Hz.
     */
    IBT2(PinName L_pwm, PinName R_pwm, PinName en, float freq);
    
    /** Set the speed and direction of the motor
     * 
     * @param speed The speed of the motor as a normalized value between -1.0 and 1.0. Use a positive value for forward and a negative value for reverse.
     */
    void setSpeed(float speed);
    
    void turnDirection(string direction , float speed);
    
    /** Get the speed and direction of the motor
     * 
     * @returns The speed of the motor as a normalized value between -1.0 and 1.0. A positive value is forward and a negative value is reverse.
     */
    float getSpeed(void);

protected:
    PwmOut _L_pwm;
    PwmOut _R_pwm;
    DigitalOut _en;
    float _period;
    float _speed;
    char _direction;
};

#endif /* MBED_IBT2_H */
