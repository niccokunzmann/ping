namespace ping
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.testbutton = new System.Windows.Forms.Button();
            this.testlabel = new System.Windows.Forms.Label();
            this.render_timer = new System.Windows.Forms.Timer(this.components);
            this.colorDialog1 = new System.Windows.Forms.ColorDialog();
            this.playfield_panel = new System.Windows.Forms.Panel();
            this.ballButton = new System.Windows.Forms.Button();
            this.updater = new System.ComponentModel.BackgroundWorker();
            this.SuspendLayout();
            // 
            // testbutton
            // 
            this.testbutton.Location = new System.Drawing.Point(12, 12);
            this.testbutton.Name = "testbutton";
            this.testbutton.Size = new System.Drawing.Size(75, 23);
            this.testbutton.TabIndex = 0;
            this.testbutton.Text = "connect";
            this.testbutton.UseVisualStyleBackColor = true;
            this.testbutton.Click += new System.EventHandler(this.button1_Click);
            // 
            // testlabel
            // 
            this.testlabel.AutoSize = true;
            this.testlabel.Location = new System.Drawing.Point(93, 17);
            this.testlabel.Name = "testlabel";
            this.testlabel.Size = new System.Drawing.Size(16, 13);
            this.testlabel.TabIndex = 1;
            this.testlabel.Text = "...";
            // 
            // render_timer
            // 
            this.render_timer.Interval = 10;
            this.render_timer.Tick += new System.EventHandler(this.timer1_Tick);
            // 
            // colorDialog1
            // 
            this.colorDialog1.SolidColorOnly = true;
            // 
            // playfield_panel
            // 
            this.playfield_panel.Location = new System.Drawing.Point(13, 42);
            this.playfield_panel.Name = "playfield_panel";
            this.playfield_panel.Size = new System.Drawing.Size(267, 216);
            this.playfield_panel.TabIndex = 2;
            this.playfield_panel.Paint += new System.Windows.Forms.PaintEventHandler(this.panel1_Paint);
            // 
            // ballButton
            // 
            this.ballButton.Location = new System.Drawing.Point(145, 12);
            this.ballButton.Name = "ballButton";
            this.ballButton.Size = new System.Drawing.Size(31, 23);
            this.ballButton.TabIndex = 3;
            this.ballButton.Text = "ball";
            this.ballButton.UseVisualStyleBackColor = true;
            this.ballButton.Click += new System.EventHandler(this.ballButton_Click);
            // 
            // updater
            // 
            this.updater.DoWork += new System.ComponentModel.DoWorkEventHandler(this.backgroundWorker1_DoWork);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(292, 270);
            this.Controls.Add(this.ballButton);
            this.Controls.Add(this.playfield_panel);
            this.Controls.Add(this.testlabel);
            this.Controls.Add(this.testbutton);
            this.Name = "Form1";
            this.Text = "Ping";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button testbutton;
        private System.Windows.Forms.Label testlabel;
        private System.Windows.Forms.Timer render_timer;
        private System.Windows.Forms.ColorDialog colorDialog1;
        private System.Windows.Forms.Panel playfield_panel;
        private System.Windows.Forms.Button ballButton;
        private System.ComponentModel.BackgroundWorker updater;
    }
}

