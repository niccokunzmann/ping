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
using System.Threading;
    

namespace ping
{
    public partial class Form1 : Form
    {

        PyroProxy playfield;
        bool connected;
        ArrayList balls;
        int counter;

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            // http://www.geoffsamuel.com/Tutorials/PaintingPanel.php
            playfield_panel.GetType().GetMethod("SetStyle",
                System.Reflection.BindingFlags.Instance |
                System.Reflection.BindingFlags.NonPublic).Invoke(playfield_panel,
                new object[]{ System.Windows.Forms.ControlStyles.UserPaint | 
                System.Windows.Forms.ControlStyles.AllPaintingInWmPaint | 
                System.Windows.Forms.ControlStyles.DoubleBuffer, true });
            connected = false;
            balls = new ArrayList();
            counter = 0;
            render_timer.Start();
            //connect();
            updater.RunWorkerAsync();
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
                    playfield_panel.Width = (int)playfield.call("get_width");
                    playfield_panel.Height = (int)playfield.call("get_height");
                    return message;
                }
            }

        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            if (connected)
            {
                
                //playfield_panel.Invalidate();
                playfield_panel.Refresh();
            }
        }

        private void update_game() {
            // http://www.dotnetperls.com/arraylist
            List<Object> server_balls = (List<Object>)playfield.call("get_balls");
            ArrayList current_balls = new ArrayList();
            foreach (PyroProxy ball in server_balls)
            {
                counter += 1;
                int x = (int)ball.call("get_x");
                int y = (int)ball.call("get_y");
                int radius = (int)ball.call("get_radius");
                current_balls.Add(new Ball(x, y, radius));
                ball.close();

            }
            this.balls = current_balls;
        }

        private void panel1_Paint(object sender, PaintEventArgs e)
        {
            // http://codesmesh.com/c-drawing-circlelinerectangle-and-ellipse-on-forms/
            Graphics g = e.Graphics;
            e.Graphics.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.HighQuality;
            if (connected)
            {
                g.Clear(Color.Green);
            }
            else
            {
                g.Clear(Color.Red);
            }
            Pen pen = new Pen(Color.Black);
            
            foreach (Ball ball in balls)
            {
                ball.Draw(g);
            }
            pen.Dispose();
            
        }

        private void ballButton_Click(object sender, EventArgs e)
        {
            playfield.call_oneway("create_ball");
        }

        private void backgroundWorker1_DoWork(object sender, DoWorkEventArgs e)
        {
            while (true)
            {
                if (connected)
                {
                    update_game();
                }
                else
                {
                    Thread.Sleep(10);
                }
            }
        }



    }
}
