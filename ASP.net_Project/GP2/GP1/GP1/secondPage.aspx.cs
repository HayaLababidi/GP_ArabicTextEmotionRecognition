using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.IO;
using System.Diagnostics;
using System.Text;

using System.Threading.Tasks;
using System.Net;
using System.Net.Sockets;

namespace GP1
{
    public partial class secondPage : System.Web.UI.Page
    {
        public string text  = " ";
        public string lable = " ";

        public Socket socket;
        protected void Page_Load(object sender, EventArgs e)
        {
            

            if (! IsPostBack)
            {
                //txt_input.Text = "yasmen";
                socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
                socket.Connect(IPAddress.Parse("127.0.0.1"), 8000);
                
                img0.Attributes.CssStyle.Add("opacity", "0.3");
                img1.Attributes.CssStyle.Add("opacity", "0.3");
                img2.Attributes.CssStyle.Add("opacity", "0.3");
                img3.Attributes.CssStyle.Add("opacity", "0.3");
                img4.Attributes.CssStyle.Add("opacity", "0.3");
                img5.Attributes.CssStyle.Add("opacity", "0.3");
                img6.Attributes.CssStyle.Add("opacity", "0.3");
                img7.Attributes.CssStyle.Add("opacity", "0.3");

                btn_predictRight.Enabled = true;
                btn_predictWrong.Enabled = true;
                list_emo.Visible = false;
            }
            
        }

        protected void btn_input_Click(object sender, EventArgs e)
        {
            img0.Attributes.CssStyle.Add("opacity", "0.3");
            img1.Attributes.CssStyle.Add("opacity", "0.3");
            img2.Attributes.CssStyle.Add("opacity", "0.3");
            img3.Attributes.CssStyle.Add("opacity", "0.3");
            img4.Attributes.CssStyle.Add("opacity", "0.3");
            img5.Attributes.CssStyle.Add("opacity", "0.3");
            img6.Attributes.CssStyle.Add("opacity", "0.3");
            img7.Attributes.CssStyle.Add("opacity", "0.3");

            //anger=0 fear=1 joy=2 love=3 natural=4 sad=5 surprised=6 sympathy=7
            text = txt_input.Text;
            string outputString ;
            

            if (text != "")
            {
                byte[] data = new byte[10000];
                socket.Send(Encoding.Unicode.GetBytes(text));
                int size = socket.Receive(data);
                outputString = Encoding.UTF8.GetString(data, 0, size);

                //anger=0 fear=1 joy=2 love=3 natural=4 sad=5 surprised=6 sympathy=7
                if (Convert.ToInt16(outputString) == 0)
                {
                    img0.Attributes.CssStyle.Add("opacity", "1");
                    lable = "anger";
                }
                else if (Convert.ToInt16(outputString) == 1)
                {
                    img1.Attributes.CssStyle.Add("opacity", "1");
                    lable = "fear";
                }
                else if (Convert.ToInt16(outputString) == 2)
                {
                    img2.Attributes.CssStyle.Add("opacity", "1");
                    lable = "joy";
                }
                else if (Convert.ToInt16(outputString) == 3)
                {
                    img3.Attributes.CssStyle.Add("opacity", "1");
                    lable = "love";
                }
                else if (Convert.ToInt16(outputString) == 4)
                {
                    img4.Attributes.CssStyle.Add("opacity", "1");
                    lable = "none";
                }
                else if (Convert.ToInt16(outputString) == 5)
                {
                    img5.Attributes.CssStyle.Add("opacity", "1");
                    lable = "sadness";
                }
                else if (Convert.ToInt16(outputString) == 6)
                {
                    img6.Attributes.CssStyle.Add("opacity", "1");
                    lable = "surprise";
                }
                else
                {
                    img7.Attributes.CssStyle.Add("opacity", "1");
                    lable = "sympathy";
                }
                 
                btn_predictRight.Enabled = true;
                btn_predictWrong.Enabled = true;
                list_emo.Visible = false;
            }
        }

        protected void btn_predictRight_Click(object sender, EventArgs e)
        {
            btn_predictWrong.Enabled = false;

            string newFileName = @"C:\GP_PythonFiles\new_EmotionalTone_dataset.csv";

            if (!File.Exists(newFileName))
            {
                string Header = "Text" + "," + "Lable" + Environment.NewLine;
                File.WriteAllText(newFileName, Header);
            }
            string content = txt_input.Text + "," + lable + Environment.NewLine;
            File.AppendAllText(newFileName, content);
        }

        protected void btn_predictWrong_Click(object sender, EventArgs e)
        {
            btn_predictRight.Enabled = false;
            list_emo.Visible = true;
        }

        protected void list_emo_SelectedIndexChanged(object sender, EventArgs e)
        {
            lable = list_emo.SelectedItem.Text;
            if (lable != "")
            {
                string newFileName = @"C:\GP_PythonFiles\new_EmotionalTone_dataset.csv";

                if (!File.Exists(newFileName))
                {
                    string Header = "Text" + "," + "Lable" + Environment.NewLine;
                    File.WriteAllText(newFileName, Header);
                }
                string content = txt_input.Text + "," + lable + Environment.NewLine;
                File.AppendAllText(newFileName, content);
            }
        }

        protected void btn_exit_Click(object sender, EventArgs e)
        {
            Server.Transfer("firstPage.aspx");
            img0.Attributes.CssStyle.Add("opacity", "0.3");
            img1.Attributes.CssStyle.Add("opacity", "0.3");
            img2.Attributes.CssStyle.Add("opacity", "0.3");
            img3.Attributes.CssStyle.Add("opacity", "0.3");
            img4.Attributes.CssStyle.Add("opacity", "0.3");
            img5.Attributes.CssStyle.Add("opacity", "0.3");
            img6.Attributes.CssStyle.Add("opacity", "0.3");
            img7.Attributes.CssStyle.Add("opacity", "0.3");
            txt_input.Text = "";
            socket.Close();

        }

        protected void list_emo_TextChanged(object sender, EventArgs e)
        {

        }
    }
}
