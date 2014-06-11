using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Drawing;

namespace ping
{
    class Ball
    {
        public int x;
        public int y;
        public int radius;

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
