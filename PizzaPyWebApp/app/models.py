class MeetupEvent:
    def __init__(self, meetup_id, title, description, event_type, images_source,
                 venue_address, venue_city, venue_postal_code, created_at, 
                 date_time, end_time, timezone, going, short_url, host_name,
                 host_username, host_email, host_member_photo, host_member_url,
                 organized_group_count):
        self.meetup_id = meetup_id
        self.title = title
        self.description = description
        self.event_type = event_type
        self.images_source = images_source
        self.venue_address = venue_address
        self.venue_city = venue_city
        self.venue_postal_code = venue_postal_code
        self.created_at = created_at
        self.date_time = date_time
        self.end_time = end_time
        self.timezone = timezone
        self.going = going
        self.short_url = short_url
        self.host_name = host_name
        self.host_username = host_username
        self.host_email = host_email
        self.host_member_photo = host_member_photo
        self.host_member_url = host_member_url
        self.organized_group_count = organized_group_count

# A list to store MeetupEvent objects (simulating in-memory storage)
events_list = []
