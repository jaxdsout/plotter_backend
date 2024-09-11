from django.core.mail import EmailMessage
from django.conf import settings
from agent.models import Profile


def send_guest_card_email(agent, client, property, interested, move_by):
    subject = f"GUEST CARD: {client.first_name} {client.last_name}"
    recipient_list = [property.email, agent.email]

    try:
        profile = Profile.objects.get(user=agent)
    except Profile.DoesNotExist:
        profile = None

    html_content = f"""
       <html>
           <body>
               <p>Hey team,</p>
               <p>Below is the guest card info for my client {client.first_name}. Please let me know if there are any issues.</p>
               <ul>
                   <li><strong>Name:</strong> {client.first_name} {client.last_name}</li>
                   <li><strong>Phone:</strong> {client.phone_number}</li>
                   <li><strong>Email:</strong> {client.email}</li>
                   <li>
                       <label><strong>Interested In:</strong></label>
                       {interested}
                   </li>
                   <li>
                       <label><strong>Move By:</strong></label>
                       {move_by}
                   </li>
               </ul>
               <p>Best,</p>
               <p>{agent.first_name} {agent.last_name if agent else 'N/A'}</p>
               <p>Licensed Real Estate Agent</p>
               <p>Phone: {profile.phone_number if profile else 'N/A'}</p>
               <p>TREC ID: {profile.trec if profile else 'N/A'}</p>               
           </body>
       </html>
    """

    email = EmailMessage(
        subject=subject,
        body=html_content,
        from_email=settings.EMAIL_HOST_USER,
        to=recipient_list
    )
    email.content_subtype = 'html'

    email.send(fail_silently=False)

