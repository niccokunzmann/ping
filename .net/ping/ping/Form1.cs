﻿using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Windows.Forms;
using Razorvine.Pyro;
using System.Collections;
using System.Threading;
    

namespace ping
{
    public partial class Form1 : Form
    {

        private PyroProxy playfield;
        private bool connected;
        private ArrayList balls;
        private ArrayList blocks;
        private PyroProxy block;
        private Keys last_press;

        public Form1()
        {
            InitializeComponent();
            this.KeyDown += f_KeyDown;
            this.KeyUp += f_KeyUp;
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
            blocks = new ArrayList();
            render_timer.Start();
            //connect();
            updater.RunWorkerAsync();
        }

        void f_KeyDown(object sender, KeyEventArgs e)
        {
            if (!connected) return;
            if (e.KeyCode == Keys.A)
            {
                block.call_oneway("move_left");
                last_press = e.KeyCode;
            }
            if (e.KeyCode == Keys.D)
            {
                block.call_oneway("move_right");
                last_press = e.KeyCode;
            }
        }
        void f_KeyUp(object sender, KeyEventArgs e)
        {
            if (last_press == e.KeyCode && connected)
            {
                block.call_oneway("move_not");
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            this.testlabel.Text = "connecting ...";
            string message;
            while (true) {
                try { 
                    message = this.connect();
                }
                catch (System.Net.Sockets.SocketException) 
                {
                    // http://stackoverflow.com/questions/12736720/how-do-you-create-a-dialog-message-box-using-asp-net
                    var msg = MessageBox.Show("Could not connect. Start the game first! Retry?", "WARNING!", MessageBoxButtons.YesNo, MessageBoxIcon.Warning, MessageBoxDefaultButton.Button2);
                    if (msg == DialogResult.Yes)
                    {
                        continue;
                    }
                    else
                    {
                        return;
                    }
                } 
                break;
            }
            this.testlabel.Text = message;
        }

        private PyroProxy new_playfield()
        {
            using (NameServerProxy ns = NameServerProxy.locateNS(null))
            {
                using (PyroProxy playfield = new PyroProxy(ns.lookup("ping.playfield")))
                {
                    return playfield;
                }
            }
        }

        private String connect()
        {
            playfield = new_playfield();
            Object result = playfield.call("test", "connected");
            string message = (string)result;  // cast to the type that 'pythonmethod' returns
            playfield_panel.Width = (int)playfield.call("get_width");
            playfield_panel.Height = (int)playfield.call("get_height");
            block = (PyroProxy)playfield.call("create_block");
            connected = true; // Pyro Proxies are not thread safe
            return message;
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            if (connected)
            {
                playfield_panel.Refresh();
            }
        }

        private void update_game() {
            update_balls();
            update_blocks();
        }

        private void update_blocks()
        {
            // http://www.dotnetperls.com/arraylist
            List<Object> proxies = (List<Object>)playfield.call("get_blocks");
            ArrayList current_blocks = new ArrayList();
            foreach (PyroProxy block in proxies)
            {
                current_blocks.Add(Block.FromPyroProxy(block));
                block.close();

            }
            this.blocks = current_blocks;
        }

        private void update_balls()
        {
            // http://www.dotnetperls.com/arraylist
            List<Object> proxies = (List<Object>)playfield.call("get_balls");
            ArrayList current_balls = new ArrayList();
            foreach (PyroProxy ball in proxies)
            {
                current_balls.Add(Ball.FromPyroProxy(ball));
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
            
            foreach (Block block in blocks)
            {
                block.Draw(g);
            }
            pen.Dispose();
            
        }

        private void ballButton_Click(object sender, EventArgs e)
        {
            PyroProxy playfield = new_playfield();
            playfield.call_oneway("create_ball");
            playfield.close();
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
