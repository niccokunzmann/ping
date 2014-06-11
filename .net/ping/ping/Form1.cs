using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using Razorvine.Pyro;
using System.Collections;
    

namespace ping
{
    public partial class Form1 : Form
    {

        PyroProxy playfield;
        bool connected;
        ArrayList balls;

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            connected = false;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            this.testlabel.Text = "connecting ...";
            string message = this.connect();
            this.testlabel.Text = message;
        }

        private String connect()
        {
            using (NameServerProxy ns = NameServerProxy.locateNS(null))
            {
                using (PyroProxy playfield = new PyroProxy(ns.lookup("ping.playfield")))
                {
                    object result = playfield.call("test", "connected");
                    string message = (string)result;  // cast to the type that 'pythonmethod' returns
                    this.playfield = playfield;
                    connected = true;
                    return message;
                }
            }

        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            if (connected) {
                render_game();
            }
        }

        private void render_game() {
            // http://www.dotnetperls.com/arraylist
            ArrayList server_balls = (ArrayList)playfield.call("get_balls");
            ArrayList current_balls = new ArrayList();
            foreach (PyroProxy ball in server_balls)
            {
                int x = (int)ball.call("get_x");
                int y = (int)ball.call("get_y");
                int radius = (int)ball.call("get_radius");
                current_balls.Add(new Ball(x, y, radius));
            }
            this.balls = current_balls;
        }

        private void panel1_Paint(object sender, PaintEventArgs e)
        {
            // http://codesmesh.com/c-drawing-circlelinerectangle-and-ellipse-on-forms/
            Graphics g = e.Graphics;
            Pen pen = new Pen(Color.Black);
            foreach (Ball ball in balls) {
                ball.Draw(pen, g);
            }
        }

    }
}
