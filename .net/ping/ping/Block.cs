using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Drawing;
using Razorvine.Pyro;
using System.Collections;

namespace ping
{
    public class Block
    {
        private int x;
        private int y;
        private int width;
        private int height;

        public static Block FromPyroProxy(PyroProxy proxy)
        {
            IDictionary values = (IDictionary)proxy.call("asDict");
            int x = (int)values["x"];
            int y = (int)values["y"];
            int width = (int)values["width"];
            int height = (int)values["height"];
            return new Block(x, y, width, height);
        }

        public Block(int x, int y, int width, int height)
	    {
            this.x = x;
            this.y = y;
            this.width = width;
            this.height = height;
	    }

        internal System.Drawing.Rectangle Rectangle()
        {
            return new System.Drawing.Rectangle(
                this.x, this.y, 
                this.width, this.height);
        }

        internal void Draw(System.Drawing.Graphics g)
        {
            g.FillRectangle(Brushes.Black, this.Rectangle());
        }
    }
}
