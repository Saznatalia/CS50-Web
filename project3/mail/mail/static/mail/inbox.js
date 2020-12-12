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
  document.querySelector('#view-email').style.display = 'none';

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
            document.querySelector('#container').style.display = 'none';
            document.querySelector('#view-email').style.display = 'none';

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
  document.querySelector('#view-email').style.display = 'none';
  document.querySelector('#container').style.display = 'block';

  // Check for an old error message, if any then remove
  if (document.querySelector('#error') != null) {
    var old_error = document.querySelector('#error');
    old_error.remove();
  }

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Load appropriate mailbox and let user click on emails to see details
  fetch(`emails/${mailbox}`, {
    method: 'GET'
  })
  .then(response => response.json())
  .then(emails => {
    document.querySelector('#container').replaceChildren();
       
    // Create all elements necessary 
    for (email in emails) {
      const email_body = document.createElement('div');
      email_body.setAttribute('id', 'email_body');
      email_body.setAttribute('class', 'email_body');
      const sender = document.createElement('div');
      const subject = document.createElement('div');
      const timestamp = document.createElement('div');
      const id = emails[email]['id'];

      // Fill innerHTML to present to user
      sender.innerHTML = 'From: ' + emails[email]['sender'];
      subject.innerHTML = emails[email]['subject'];
      timestamp.innerHTML = emails[email]['timestamp'];
      if (mailbox === 'sent') {
        sender.innerHTML = emailbox = 'To: ' + emails[email]['recipients'];
      }

      // Style elements
      sender.style.fontWeight = 'bold';
      sender.style.width = '30vw';
      subject.style.width = '50vw';
      timestamp.style.color = 'darkgrey';
      timestamp.style.width = '30vw';  
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
      email_body.addEventListener('click', () => load_email(id, mailbox));
      document.querySelector('#container').append(email_body);     
    }
  });
};

function load_email(id, mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#container').style.display = 'none';
  document.querySelector('#view-email').style.display = 'block';
  
  // Check for an old error message, if any then remove
  if (document.querySelector('#error') != null) {
    var old_error = document.querySelector('#error');
    old_error.remove();
  }

  // Mark email "read" once it was clicked
  fetch(`emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  });

  // Present details of the email to user
  fetch(`emails/${id}`, {
    method: 'GET'
  })
  .then(response => response.json())
  .then(email => {
    document.querySelector('#view-email').replaceChildren();

    // Create new elements to display email details to user
    const sender = document.createElement('div');
    const recipients = document.createElement('div');
    const subject = document.createElement('div');
    const timestamp = document.createElement('div');
    const body = document.createElement('pre');
    const reply_button = document.createElement('button');
    reply_button.setAttribute('class', 'btn btn-sm btn-outline-primary');
    reply_button.setAttribute('id', 'reply_button');
    const archive_button = document.createElement('button');
    archive_button.setAttribute('class', 'btn btn-sm btn-outline-primary');
    archive_button.setAttribute('id', 'archive_button');
    const unarchive_button = document.createElement('button');
    unarchive_button.setAttribute('class', 'btn btn-sm btn-outline-primary');
    unarchive_button.setAttribute('id', 'unarchive_button');

    // Set up inner html of each element, i.e. what is going to be displayed
    sender.innerHTML = 'From: ' + email['sender'];
    recipients.innerHTML = 'To: ' + email['recipients']
    subject.innerHTML = 'Subject: ' + email['subject'];
    timestamp.innerHTML = 'Timestamp: ' + email['timestamp'];
    body.innerHTML = email['body'];
    body.setAttribute('class', 'body');
    reply_button.innerHTML = 'Reply';
    reply_button.addEventListener('click', () => reply(email));
    archive_button.innerHTML = 'Archive';
    archive_button.addEventListener('click', () => archive(id));
    unarchive_button.innerHTML = 'Unarchive';
    unarchive_button.addEventListener('click', () => unarchive(id));

    // Add above elements to the html body
    document.querySelector('#view-email').appendChild(sender);
    document.querySelector('#view-email').appendChild(recipients);
    document.querySelector('#view-email').appendChild(subject);
    document.querySelector('#view-email').appendChild(timestamp);
    document.querySelector('#view-email').appendChild(body);
    
    // If inbox add 2 buttons "archive" and "reply", if archive add 1 button "unarchive"   
    if (mailbox === 'inbox') {
      document.querySelector('#view-email').appendChild(reply_button);
      document.querySelector('#view-email').appendChild(archive_button);
    }
    if (mailbox === 'archive') {
      document.querySelector('#view-email').appendChild(unarchive_button);
    }
  });
}

// Reply function
function reply(email) {
  compose_email();

  // Pre-fill required composition fields
  document.querySelector('#compose-recipients').value = email['sender'];
  if (email['subject'].substring(0,3) != "Re:") {
    email['subject'] = 'Re: ' + email['subject'];
  }
  document.querySelector('#compose-subject').value = email["subject"]
  document.querySelector('#compose-body').value = '\n\n-----On ' + email['timestamp'] + ' ' + email['recipients'] + ' wrote: ' + email['body'];
}

// Archive email function
function archive(id) {
  fetch(`emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: true
    })
  })
  .then(() => {
    load_mailbox('inbox');
  })    
}

// Unarchive email function
function unarchive(id) {
  fetch(`emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: false
    })
  })
  .then(() => {
    load_mailbox('inbox');
  })    
}
