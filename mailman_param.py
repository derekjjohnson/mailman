class Mailman():

    def __init__(self):
        self.twilio_acct_sid = ""
        self.twilio_auth_token = ""
        self.twilio_number = ""
        self.particle_device = ""
        self.particle_token = ""
        self.url_string = ""
        self.mqtt_url = ""
        self.mqtt_queue = ""
        self.get_mailman()
        pass


    def set_params(self, twilio_acct_sid, twilio_auth_token, twilio_number, particle_device, particle_token):
        self.twilio_acct_sid = twilio_acct_sid
        self.twilio_auth_token = twilio_auth_token
        self.twilio_number = twilio_number
        self.particle_device = particle_device
        self.particle_token = particle_token
        self.url_string = "https://api.particle.io/v1/devices/" + self.particle_device + "/mailbox?access_token=" + self.particle_token
        self.mqtt_url = "broker.hivemq.com"
        self.mqtt_queue = "djmailman/#"
        pass


    def get_mailman(self):
        # This URL lets me get a Particle.variable value
        particle_device = "XXXXXXXXXXXXXXXXXXXX"
        particle_token = "XXXXXXXXXXXXXXXXXXXXX"
        # Your Account SID from twilio.com/console
        account_sid = "XXXXXXXXXXXXXXXXXXXXX"
        # Your Auth Token from twilio.com/console
        auth_token = "XXXXXXXXXXXXXXXXXXXXX"
        # Your Twilio number for sending an SMS
        twilio_number = "+18885551212"
        # Your list of numbers to send an SMS notification
        call_list = ["+17635551212"]
        self.set_params(account_sid, auth_token, twilio_number, particle_device, particle_token)
        # print(self.url_string)
        pass
