let id_mensaje = 0;
let controller = null;
let url = 'https://fastapi-chatbot-gobierno-jalisco.onrender.com/api/v1/';
let procedures = [];
let index_procedure_selected = null;

// --------------------------------------------------
//                    functions
// --------------------------------------------------

function format_chatbot_mesage(id){

  const chatbotMessage = `
  <div class='chatbot-message col-12 py-4 d-flex justify-content-center' id='${id}' style='display:none;'>
      <div class='d-flex col-8' id='chatbot-message-content'>
          <img src='static/imgs/chatbot.png' width='40' height='40'>
          <div class='m-2'>
              <h6>Ágil bot</h6>
              <div class='container-animacion'>
                <div class='cargando'>
                  <div class='pelotas'></div>
                  <div class='pelotas'></div>
                  <div class='pelotas'></div>
                </div>
              </div>
          </div>
      </div>
  </div>`;

  return chatbotMessage;

}


function format_user_mesage(message){

  const userMessage = `
  <div class='user-message col-12 py-4 d-flex justify-content-center'>
      <div class='d-flex col-8' id='user-message-content'>
          <img src='static/imgs/user.png' width='40' height='40'>
          <div class='m-2'>
              <h6>Tú</h6>
              <p>${message}</p>
          </div>
      </div>
  </div>`;

  return userMessage;

}


function disable_form_message(){
  $('#btn-detener').show();
  $('#btn-enviar').hide();
  $('#input-message').prop('disabled', true);
}


function disable_form_search(){
  $('#input-search').prop('disabled', true);
}


function enable_form_message(){
  let send_button = $('#btn-enviar');
  send_button.css('color', '#000000');
  send_button.css('background-color', '#c5c5c5');
  send_button.prop('disabled', true);
  send_button.show();
  $('#btn-detener').hide();
  $('#input-message').prop('disabled', false);
}


function enable_form_search(){
  $('#input-search').prop('disabled', false);
}


async function add_procedures(data){

  data.forEach((element, index) => {

    const name = element['name'];
    procedures.push(element);

    $(".offcanvas-body").append(`
	    <div onclick="select_procedure('${index}', '${name}')" class="procedure-container" id="${index}">
		    ${name}
	    </div>
	    <br>
    `);
  });
}


async function add_filtered_procedures(data){

  data.forEach((element, index) => {

    const name = element['name'];

    $(".offcanvas-body").append(`
	    <div onclick="select_procedure('${index}', '${name}')" class="procedure-container" id="${index}">
		    ${name}
	    </div>
	    <br>
    `);
  });
}


async function get_procedures(){
  const get_procedures_url = url+'procedures';

  const response = await fetch(get_procedures_url, {
    method: 'GET',
  }).then(response => response.json())
    .then(data => data)
  
  add_procedures(response);

  return response;
}


async function initialize(){
  disable_form_search();
  await get_procedures();
  enable_form_search();
  let send_button = $('#btn-enviar');
  send_button.css('background-color', '#c5c5c5');
  send_button.css('color', '#000000');
  send_button.prop('disabled', true);
  $('#btn-detener').hide();
}


function get_message(){
  const message = $('#input-message').val();
  $('#input-message').val('');
  return message;
}


async function send_message(message, signal){
  const send_message_url = url+'chatbot/msg';
  //let url = '';
  const response = await fetch(send_message_url, {
    signal: signal,
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      msg:message,
      thread_id:localStorage.getItem('thread_id'),
      procedure:procedures[index_procedure_selected]['name']})
  }).then(response => response.json())
    .then(data => data
    ).catch(error => {
      return {'msg':'<h7 class="text-danger">Hubo un error en el mensaje<h7>'};
    });

  return response;
}


async function delete_conversation_thread(){
	var requestOptions = {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		}
	};

  const thread_url = url+'chatbot/thread_id/'+localStorage.getItem('thread_id')
	navigator.sendBeacon(thread_url, requestOptions);

	localStorage.removeItem('thread_id');
}


async function create_conversational_thread(){
  const thread_url = url+'chatbot/thread_id';
  //let url = '';
  const response = await fetch(thread_url, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  }).then(response => response.json())
    .then(data => data
    ).catch(error => {
      return {'msg':'<h7 class="text-danger">Error, no se ha podido establecer una conversacion<h7>'};
    });

  return response;
}


async function select_procedure(index, text){

  const response = await create_conversational_thread();
  localStorage.setItem('thread_id', response['thread_id']);
	index_procedure_selected = index;
  $(".offcanvas").offcanvas('hide');

}


// --------------------------------------------------
//                      events
// --------------------------------------------------

$('#input-message').on('keyup', function(event){

  let text = $(this).val();
  let button = $('#btn-enviar');

  if(text.trim() === ""){
    button.css('color', '#000000');
    button.css('background-color', '#c5c5c5');
    button.prop('disabled', true);
  }else{
    if (event.keyCode === 13) {
      button.trigger('click');
    }

    button.css('color', '#ffffff');
    button.css('background-color', '#007bff');
    button.prop('disabled', false);
  }

});


$('#btn-menu').on('click', async function(){
  $(".conversation").html(`
  <div class="chatbot-message col-12 py-4 d-flex justify-content-center">
    <div class="d-flex col-8" id="chatbot-message-content">
      <img src="static/imgs/chatbot.png" width="40" height="40">
      <div class="m-2">
        <h6>Ágil bot</h6>
        <p>👋 ¡Hola! y Bienvenido al portal de consultas de trámites del gobierno de Jalisco. Pregúntame lo que necesites sabes sobre este trámite.</p>
      </div>
    </div>
  </div>
	<br>
  `);
  await delete_conversation_thread();
})

$(window).on('beforeunload', async function() {
  if(localStorage.getItem('thread_id')!==null){
    await delete_conversation_thread();
  }
});

$('#btn-enviar').on('click', async function(){

  disable_form_message();
  const userMessage = get_message();

  // getting identifier to add in chatbot message
  const id = 'container-chatbot-message-'+id_mensaje++;
  const formattedChatbotMessage = format_chatbot_mesage(id);
  const formattedUserMessage = format_user_mesage(userMessage);

  // adding messages to conversation
  $('.conversation').append(formattedUserMessage);
  $('.conversation').append(formattedChatbotMessage);

  window.scrollTo(0, document.documentElement.scrollHeight);

  // sending message to chatbot
  controller = new AbortController();
  const signal = controller.signal;
  const response = await send_message(userMessage, signal);

  // adding bot message to conversation
  $('.container-animacion').remove();
  $(`#${id}`).fadeIn();
  const converter = new showdown.Converter();
  const htmlOutput = converter.makeHtml(response['msg']);

  let images = '';

  if(response['images']){
    response['images'].forEach(image => {
      images += `<img src='${image}' class='rounded float-left img-thumbnail' width='200' height='200'>`;
    });
  }

  $(`#${id} .m-2`).append(`<p>
    ${htmlOutput}
    ${images}
  </p>`);

  window.scrollTo(0, document.documentElement.scrollHeight);

  enable_form_message();

});


$('#btn-detener').on('click', function(){
  enable_form_message();
  if (controller) {
    controller.abort(); // Se llama al método abort() del controlador para cancelar la petición
    console.log('Petición cancelada');
  }
});


$("#input-search").on("input", function(event) {

  $('.offcanvas-body').html('');

  let text = $(this).val();
  let filtered_data_procedure = []

  for (const procedure of procedures) {
    if (procedure['name'].includes(text)) {  // Usando `includes()` para búsqueda simple
      filtered_data_procedure.push(procedure);
    }
  }

  add_filtered_procedures(filtered_data_procedure);

});

// --------------------------------------------------
//                 initialization
// --------------------------------------------------

$(document).ready(async function() {
  await initialize();

  $(".loader-wrapper").fadeOut(1200, function() {
    $("#contenido").fadeIn(1500);
  });
});


//$( document ).ready(function(){});
//$( window ).on( "load", function(){});