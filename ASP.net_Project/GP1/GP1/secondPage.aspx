<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="secondPage.aspx.cs" Inherits="GP1.secondPage" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml" lang="en">

<head id="Head1" runat="server">
   <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="">
  <meta name="author" content="">
  <title>Emotion Detect From Arabic Text</title>
  <link href="css/bootstrap.min.css" rel="stylesheet">
  <link href="css/animate.min.css" rel="stylesheet"> 
  <link href="css/font-awesome.min.css" rel="stylesheet">
  <link href="css/lightbox.css" rel="stylesheet">
  <link href="css/main.css" rel="stylesheet">
  <link id="csspreset" href="css/presets/preset1.css" rel="stylesheet">
  <link href="css/responsive.css" rel="stylesheet">

  <!--[if lt IE 9]>
    <script src="js/html5shiv.js"></script>
    <script src="js/respond.min.js"></script>
  <![endif]-->
  
  <link href='http://fonts.googleapis.com/css?family=Open+Sans:300,400,600,700' rel='stylesheet' type='text/css'>
  <link rel="shortcut icon" href="images/favicon.ico">
</head>
<body>
    <form id="form1" runat="server">
    <div>
    <!--.preloader-->
  <div class="preloader"> <i class="fa fa-circle-o-notch fa-spin"></i></div>
  <!--/.preloader-->
    </div><!--/#home-slider-->
    <div class="main-nav">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>                   
        </div>
        <div class="collapse navbar-collapse">
          <ul class="nav navbar-nav navbar-right">  
            <li class="scroll"><a href="firstPage.aspx">Home</a></li>                
            <li class="scroll"><a href="#services">Service</a></li> 
          </ul>
            <p>Emotion Detection From Arabic Text</p>
        </div>
      </div>
    </div><!--/#main-nav-->
  <section id="services">
    <div class="container">
      <div class="heading wow fadeInUp" data-wow-duration="1000ms" data-wow-delay="300ms">
        <div class="row">
          <div class="text-center col-sm-8 col-sm-offset-2">
            <h2>Our Service</h2>
            <p>تنبؤ المشاعر من نص عربي</p>
          </div> 
                    <div class="row">
							<div class="col-sm-9">
                                <!-- the input -->
                                <label for="inputText">ادخل جملة لمعرفة حالتها</label>                           
                                <asp:TextBox ID="txt_input" runat="server" class="form-control"></asp:TextBox>     
							</div>
						</div><br>
              
                    <div class="row">
							<div class="col-sm-9">
                                <asp:Button ID="btn_input" runat="server" Text="تحليل" OnClick="btn_input_Click" class="btn btn-primary"/>
							</div>
						</div><br>
                  	                 
                         <!-- the output -->         
						<div class="container-fluid result">
							<div class="row emo-ji emotion">

                                <div class="col-sm-2" data-emotion="angry">
									<img runat="server" id="img0" src="images/emoji/angry.png">
									<p>غضب</p>
								</div>
                                <div class="col-sm-2" data-emotion="fear">
									<img runat="server" id="img1" src="images/emoji/fear.png">
									<p>خوف</p>
								</div>
								<div class="col-sm-2" data-emotion="happy">
									<img runat="server" id="img2" src="images/emoji/happy.png" class="img-fluid">
									<p>فرح</p>
								</div>
                                <div class="col-sm-2" data-emotion="love">
									<img runat="server" id="img3" src="images/emoji/love.png">
									<p>حب</p>
								</div>
								<div class="col-sm-2" data-emotion="Neutral">
									<img runat="server" id="img4" src="images/emoji/Neutral.png">
									<p>طبيعي</p>
								</div>
                   				<div class="col-sm-2" data-emotion="sad">
									<img runat="server" id="img5" src="images/emoji/sad.png">
									<p>حزن</p>
								</div>
								<div class="col-sm-2" data-emotion="Surprised">
									<img runat="server" id="img6" src="images/emoji/Surprised.png">
									<p>مفاجئة</p>
								</div>
                                <div class="col-sm-2" data-emotion="Sympathy">
									<img runat="server" id="img7" src="images/emoji/Sympathy.png">
									<p>تعاطف</p>
								</div>
							</div>
						</div>
        </div> 

           <!-- the check -->
            <div class="row">
		    <div class="col-sm-9">   
                <asp:Button ID="btn_predictRight" runat="server" Text="تنبؤ صحيح" OnClick="btn_predictRight_Click" class="btn btn-success"/>
                <asp:Button ID="btn_predictWrong" runat="server" Text="تنبؤ خاطئ" OnClick="btn_predictWrong_Click" class="btn btn-danger"/>
            
                 <asp:DropDownList ID="list_emo" runat="server" Width="200px" AutoPostBack = "true" OnSelectedIndexChanged ="list_emo_SelectedIndexChanged">
                    <asp:ListItem Text="فرح" Value="1" />
                    <asp:ListItem Text="غضب" Value="2" />
                    <asp:ListItem Text="مفاجئة" Value="3" />
                    <asp:ListItem Text="حزن" Value="4" />
                    <asp:ListItem Text="خوف" Value="5" />
                    <asp:ListItem Text="طبيعي" Value="6" />
                    <asp:ListItem Text="حب" Value="7" />
                    <asp:ListItem Text="نعاطف" Value="8" />
                </asp:DropDownList> 
		    </div>
	</div>
      </div>
      </div>

  </section><!--/#services-->

  <footer id="footer">
    <div class="footer-top wow fadeInUp" data-wow-duration="1000ms" data-wow-delay="300ms">
    </div>
    <div class="footer-bottom">
      <div class="container">
        <div class="row">
          <div class="col-sm-6">
            <p>&copy; 2019 Graduation Project.</p>
          </div>
        </div>
      </div>
    </div>
  </footer>

  <script type="text/javascript" src="js/jquery.js"></script>
  <script type="text/javascript" src="js/bootstrap.min.js"></script>
  <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=true"></script>
  <script type="text/javascript" src="js/jquery.inview.min.js"></script>
  <script type="text/javascript" src="js/wow.min.js"></script>
  <script type="text/javascript" src="js/mousescroll.js"></script>
  <script type="text/javascript" src="js/smoothscroll.js"></script>
  <script type="text/javascript" src="js/jquery.countTo.js"></script>
  <script type="text/javascript" src="js/lightbox.min.js"></script>
  <script type="text/javascript" src="js/main.js"></script>
    </div>
    </form>
</body>
</html>
