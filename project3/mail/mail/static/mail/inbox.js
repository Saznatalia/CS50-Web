document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#container').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  
  // Check for an old error message, if any then remove
  if (document.querySelector('#error') != null) {
    var old_error = document.querySelector('#error');
    old_error.remove();
  }
    
  // Listen for submission of form
  document.querySelector('form').onsubmit = function(event) {
    event.preventDefault();
    
    // Find recipients, subject and body of email submitted
    const recipients = document.querySelector("#compose-recipients").value;
    const subject = document.querySelector("#compose-subject").value;
    const body = document.querySelector("#compose-body").value;

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    })
      .then(response => {
        return response.json().then(result => {

          // Check if the email is sent successfully load the user's sent mailbox
          if (response.status === 201) {
            load_mailbox('sent');
          }

          // If error print result
          else {
            console.log(result['error']);
            
            // Hide all views
            document.querySelector('#emails-view').style.display = 'none';
            document.querySelector('#compose-view').style.display = 'none';

            // Clear out composition fields
            document.querySelector('#compose-recipients').value = '';
            document.querySelector('#compose-subject').value = '';
            document.querySelector('#compose-body').value = '';

            // Create an error message to display to user
            var error_div = document.createElement('div');
            error_div.setAttribute('id', "error");
            error_div.innerHTML = result['error'];
            document.body.appendChild(error_div);
            document.querySelector('#error').style.color = 'red';
            document.querySelector('#error').style.fontSize = '26px';
            document.querySelector('#error').style.textAlign = 'center'; 
          }
        })
      })
  }
}

function load_mailbox(mailbox) {
 
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#container').style.display = 'block';

  
  // Check for an old error message, if any then remove
  if (document.querySelector('#error') != null) {
    var old_error = document.querySelector('#error');
    old_error.remove();
  }

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`emails/${mailbox}`, {
    method: 'GET'
  })
  .then(response => response.json())
  .then(emails => {
    console.log(emails);
    document.querySelector('#container').replaceChildren();
        
    // Display styled elements to user 
    for (email in emails) {
      const email_body = document.createElement('div');
      email_body.setAttribute('id', 'email_body');
      email_body.setAttribute('class', 'email_body');
      const sender = document.createElement('div');
      const subject = document.createElement('div');
      const timestamp = document.createElement('div');

      sender.innerHTML = emails[email]['sender'];
      subject.innerHTML = emails[email]['subject'];
      timestamp.innerHTML = emails[email]['timestamp'];

      // Style elements
      sender.style.fontWeight = 'bold';
      sender.style.width = '20vw';
      subject.style.width = '50vw';
      timestamp.style.color = 'darkgrey';
      timestamp.style.width = '27vw';  
      timestamp.style.textAlign = 'right';
      if (emails[email]['read'] == false) {
        email_body.style.backgroundColor = 'white';
      }
      else {
        email_body.style.backgroundColor = "lightgrey"
      }

      // Add elements to the html body
      email_body.appendChild(sender);
      email_body.appendChild(subject);
      email_body.appendChild(timestamp);
      email_body.addEventListener('click', () => load_email());
      document.querySelector('#container').append(email_body);
    }
  });
};

function load_email() {

  console.log('This element has been clicked!');
}
