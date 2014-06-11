using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

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
                this.x + this.radius, this.y + this.radius);
        }

        internal void Draw(System.Drawing.Pen pen, System.Drawing.Graphics g)
        {
            pen.Color = System.Drawing.Color.Black;
            g.DrawEllipse(pen, Rectangle());
        }
    }
}
