﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Drawing;
using Razorvine.Pyro;
using System.Collections;

namespace ping
{
    class Ball
    {
        public int x;
        public int y;
        public int radius;

        public static Ball FromPyroProxy(PyroProxy proxy)
        {
            IDictionary values = (IDictionary)proxy.call("asDict");
            int x = (int)values["x"];
            int y = (int)values["y"];
            int radius = (int)values["radius"];
            return new Ball(x, y, radius);
        }

        public Ball(int x, int y, int radius)
        {
            this.x = x;
            this.y = y;
            this.radius = radius;
        }


        internal System.Drawing.Rectangle Rectangle()
        {
            return new System.Drawing.Rectangle(
                this.x - this.radius, this.y - this.radius, 
                2 * this.radius, 2 * this.radius);
        }

        internal void Draw(System.Drawing.Graphics g)
        {
            g.FillEllipse(Brushes.Blue, this.Rectangle());
        }
    }
}
