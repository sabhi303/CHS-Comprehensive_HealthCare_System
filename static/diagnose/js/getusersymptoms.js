var symps = new Array();
var currentpage=2;
function delThis(num) {
    var index = symps.indexOf(num);
    if (index > -1) {
        symps.splice(index, 2);
        $("#" + num).remove();
    }
    getsuggestions();
}

// function addThis(x) {


//     var node = document.getElementById("suggestedSymps");
//     node.querySelectorAll('*').forEach(n => n.remove());



//     symps.push(x);
//     symps.push('1');
//     document.getElementById("myInput").value = '';
//     var strstsr = '<button id=' + x + " style='color:green;' class='btn btn-outline-secondary text-center m-1' onclick=delThis('" + x + "')>" + x + "</button>";

//     $("#AddSympsHere").append(strstsr);
//     getsuggestions();

// }

function addUserSymps(color="green") {
  // alert(symps);
    var x = document.getElementById("myInput").value;
    symps.push(x);
    if(color=="green")
      symps.push('1');
    else
      symps.push('0');
    document.getElementById("myInput").value = '';
      let strstsr = `<button type="button" id=` + x + ` style=" color: `+ color+ `;" class="btn alert alert-success" data-dismiss="alert" onclick=delThis('` + x + `') aria-label="Close">
      <span>`+ x + `</span>
        </button>`
        $("#AddSympsHere").append(strstsr);
    
    getsuggestions();
}


// document.getElementById("adduserSympButton").addEventListener("click", addUserSymps);
function addyes(){
    var x=document.getElementById("yes").value;
    addSuggestedSymp(x,"green");
    // symps.push(x);
    // symps.push('1');
    // document.getElementById("myInput").value = '';
    // var strstsr = '<button id=' + x + " style='color:green;' class='btn btn-outline-secondary text-center m-1' onclick=delThis('" + x + "')>" + x + "</button>";

    // $("#AddSympsHere").append(strstsr);
    // qa();
}
function addno(){
    var x=document.getElementById("no").value;
    addSuggestedSymp(x,"red");
    // symps.push(x);
    // symps.push('0');
    // document.getElementById("myInput").value = '';
    // var strstsr = '<button id=' + x + " style='color:red;' class='btn btn-outline-secondary text-center m-1' onclick=delThis('" + x + "')>" + x + "</button>";

    // $("#AddSympsHere").append(strstsr);
    // qa();
}


function suggestSymptoms(a) {


  $("#suggesionss").empty();
    
  //ithe fkt max 5 suggestions thev not more than that

  let strstsr = `<div class="sugestionsclass"> 
  Here are some <br> suggestions for you!<br>
                  </div>
                  `

  $("#suggesionss").append(strstsr);

    //hyat to array access krun yash chya decision tree la dyayachay
    // var node = document.getElementById("suggestedSymps");
    // node.querySelectorAll('*').forEach(n => n.remove());

    // var st= '<button class="btn text-center m-1" style="border:none; background-color:#f8f9fa;">Suggested:</p>';
    // $("#suggestedSymps").append(st);

    // alert(a);
    if(a[0]=="nosymp"){
      // var st= '<button class="btn text-center m-1" style="border:none; background-color:#f8f9fa;">None</p>';
      // $("#suggestedSymps").append(st);
      var x=`<button type="button" class="btn alert alert-success" data-dismiss="alert"  aria-label="Close" disabled>
                      <span> None </span> 
                  </button> <br>`;
      $('.sugestionsclass').append(x);
    }
    else{
      for(var i=0;i<a.length;i++){
          // var strstsr = '<button id=' + a[i] + " class='btn btn-outline-secondary text-center m-1' onclick=addThis('" + a[i] + "')>" + a[i] + "</button>";
          // //he vrcha system kdun ghyaychay for now let it be
          // $("#suggestedSymps").append(strstsr);

          var x=` <button type="button" class="btn alert alert-success" data-dismiss="alert" onclick=addSuggestedSymp('`+ a[i] + `') aria-label="Close">
                    <span>`+ a[i] + `</span> 
                  </button> <br>`;
      $('.sugestionsclass').append(x);

      }
    }
}

function addSuggestedSymp(x,color="green") {
  $("#suggesionss").empty();
  document.getElementById("myInput").value = x;
  addUserSymps(color);
}

// function qa(){
//   alert("asach");
//     document.getElementById("normal").style.display="none";
//     document.getElementById("qa").style.display="block";
//     $.ajax({
//         type : 'POST',
//         url : "suggest",
//         data:{
//           "symptoms": symps.toString(),
//           csrfmiddlewaretoken: '{{ csrf_token }}',
//         },
//         success : function(data){
//           data=JSON.parse(data);
//           if(symps.toString()!=data["before"].toString()){
//             alert("skip");
//           }
//           else{
//             var sugesstions=data["after"];
//             alert(sugesstions);
//             if(sugesstions[0]=='nosymp'){
//                 // alert("Result : "+sugesstions[1]);
//                 //this is diagnosis result by decision tree
//                 document.getElementById("question").innerHTML="Done with suggestions!!";
//             }
//             else{
//               document.getElementById("question").innerHTML="Are you experincing "+sugesstions[0]+"?";
//               $('#yes').attr('value', sugesstions[0]);
//               $('#no').attr('value', sugesstions[0]);
//             }
//           }
//         }
//       });
// }
// function normal(){
//   alert('in');
//     document.getElementById("normal").style.display="block";
//     document.getElementById("qa").style.display="none";
//     getsuggestions();

// }
// document.getElementById("profile-tab").addEventListener("click", qa)
// document.getElementById("home-tab").addEventListener("click", normal)

function getsuggestions(){
  // alert(symps);
  // alert(num);
  if(currentpage==2){
    $('#suggesionss').empty();
    let strs=` <h5 class="pt-3">&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;Suggestions are &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; loading.... &nbsp;&nbsp;&nbsp;&nbsp;</h5>
    <svg class="logoimage" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"  style="margin-left:100px !important;">
    <path fill="none" stroke="#e90c59" stroke-width="8" stroke-dasharray="42.76482137044271 42.76482137044271" d="M24.3 30C11.4 30 5 43.3 5 50s6.4 20 19.3 20c19.3 0 32.1-40 51.4-40 C88.6 30 95 43.3 95 50s-6.4 20-19.3 20C56.4 70 43.6 30 24.3 30z" stroke-linecap="round" style="transform:scale(0.8);transform-origin:50px 50px">
      <animate attributeName="stroke-dashoffset" repeatCount="indefinite" dur="1s" keyTimes="0;1" values="0;256.58892822265625"></animate>
    </path>`;
        $('#suggesionss').append(strs);
  //   $('#suggesionss').append(`<div class="sugestionsclass"> 
  // Here are some <br> suggestions for you!<br>
  //                 </div>
  //                 `);
  //   $('.sugestionsclass').append(`<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"  style="margin: auto; text-algn:center; display: block; shape-rendering: auto;" width="100px" height="100px" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
  //   <path fill="none" stroke="#e90c59" stroke-width="8" stroke-dasharray="42.76482137044271 42.76482137044271" d="M24.3 30C11.4 30 5 43.3 5 50s6.4 20 19.3 20c19.3 0 32.1-40 51.4-40 C88.6 30 95 43.3 95 50s-6.4 20-19.3 20C56.4 70 43.6 30 24.3 30z" stroke-linecap="round" style="transform:scale(0.8);transform-origin:50px 50px">
  //     <animate attributeName="stroke-dashoffset" repeatCount="indefinite" dur="1s" keyTimes="0;1" values="0;256.58892822265625"></animate>
  //   </path>`);
  }
  else{
    $('#question').empty();
    let strs=` <h5 class="pt-3">&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;Suggestions are  loading.... &nbsp;&nbsp;&nbsp;&nbsp;</h5>
    <svg xmlns="http://www.w3.org/2000/svg" class="text-center" xmlns:xlink="http://www.w3.org/1999/xlink" style="margin-left:42%;margin-top:40px;margin-bottom:40px;">
    <path fill="none" stroke="#e90c59" stroke-width="8" stroke-dasharray="42.76482137044271 42.76482137044271" d="M24.3 30C11.4 30 5 43.3 5 50s6.4 20 19.3 20c19.3 0 32.1-40 51.4-40 C88.6 30 95 43.3 95 50s-6.4 20-19.3 20C56.4 70 43.6 30 24.3 30z" stroke-linecap="round" style="transform:scale(0.8);transform-origin:50px 50px">
      <animate attributeName="stroke-dashoffset" repeatCount="indefinite" dur="1s" keyTimes="0;1" values="0;256.58892822265625"></animate>
    </path>`;
      $('#question').append(strs);
    $("#yes").hide();
    $("#no").hide();
  }
    $.ajax({
        type : 'POST',
        url : "suggest",
        data:{
          "symptoms": symps.toString(),
          csrfmiddlewaretoken: '{{ csrf_token }}',
        },
        success : function(data){
          // alert(data);
          data=JSON.parse(data);
          // alert(data);
          // alert(symps.toString());
          // alert(data["after"]);
          // alert(data["before"].toString());
          if(symps.toString()!=data["before"].toString()){
            // alert("skip");
          }
          else{
            sugesstions=data["after"];
            // alert(sugesstions);
            if(currentpage==1){
              if(sugesstions[0]=='nosymp'){
                document.getElementById("question").innerHTML="Done with suggestions!!";
                $("#yes").prop('disabled', true);
                $("#no").prop('disabled', true);
              }
              else{
                document.getElementById("question").innerHTML="Are you experincing "+sugesstions[0]+"?";
                $('#yes').attr('value', sugesstions[0]);
                $('#no').attr('value', sugesstions[0]);
                $("#yes").show();
                $("#no").show();
              }
            }
            else{
              sugesstions=data["after"];
              // alert(sugesstions);
              suggestSymptoms(sugesstions);
            }
          }
        }
      });

}

function changeContent(num) {
  // alert(num);
  if (num == 1) {
      //ithe ulti chya thikani symptom taak
      $("#inputsearchbar").hide();
      $("#quesanswers").show();
      currentpage=1;
      
      $('#changeContentButt').html('Enter Sypmtoms');
      $("#changeContentButt").attr("onclick", "changeContent(2)");

      let strstr = `
      <h5 class="pt-3">&nbsp;&nbsp;&nbsp;&nbsp;Not sure what's &nbsp;&nbsp;&nbsp;&nbsp;happening?</h5>
      <img class="logoimage" src="../../static/diagnose/image/dTree.png">
      <h6 class="text-center">We'll suggest you something using our decision tree..<br>
          &nbsp;&nbsp;&nbsp;Add any one symptom to get started!</h6>
      `;
      $("#suggesionss").empty();
      $("#suggesionss").append(strstr);
  }
  else {
      currentpage=2;
      $("#quesanswers").hide();
      $("#inputsearchbar").show();

      $('#changeContentButt').html('Prefer Questions?');
      $("#changeContentButt").attr("onclick", "changeContent(1)");
  }
  getsuggestions();
}

function diagnoseit(){

  if(symps.length==0){
    alert("Enter atleast one symptom");
  }
  else{
    $('#preloader-active').show();
    var final='';
    for(var i=0;i<symps.length;i++){
      final+=symps[i]+',';
    }
    
    final=final.slice(0,-1);
    // alert(final);
    $("#symptoms").val(final);
    // alert($("#symptoms").val());
    $("#digform").submit();

  }
}