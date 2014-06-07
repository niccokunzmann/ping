using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using Razorvine.Pyro;
    

namespace ping
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
    
        }

        private void button1_Click(object sender, EventArgs e)
        {
            this.testlabel.Text = "testing ...";
            string message = this.test();
            this.testlabel.Text = message;
        }

        private String test()
        {
            using (NameServerProxy ns = NameServerProxy.locateNS(null))
            {
                using (PyroProxy something = new PyroProxy(ns.lookup("ping.playfield")))
                {
                    object result = something.call("test", 42, "hello", new int[] { 1, 2, 3 });
                    string message = (string)result;  // cast to the type that 'pythonmethod' returns
                    return message;
                }
            }

        }
    }
}
