from flask import Flask, request
from flask import render_template
from googleapiclient.discovery import build

app = Flask(__name__)
service = build('civicinfo', b'v2', developerKey='AIzaSyALXTo54A8rFTsrMnT2AT6SUMS5mI4Qn9k');
collection = service.representatives();

@app.route('/', methods=['GET','POST'])
def main():
	if request.method == 'POST':
		address = request.form.get('address')
		print(address);
		request_api = collection.representativeInfoByAddress(levels=['administrativeArea1','country'], roles=['headOfGovernment','legislatorLowerBody','legislatorUpperBody'], address=address, includeOffices=None)
		response = request_api.execute()
		officials = response['officials']
		offices = response['offices']
		divisions = response['divisions']

		reps = get_reps(officials, offices, divisions);
		reps = sorted(reps, key=lambda k: k['officeIndex'], reverse=True)

		return render_template('messaging_templates.html', reps=reps)

	return render_template('index.html')

@app.route('/messaging_templates')
def messaging_templates():
	return render_template('messaging_templates.html')

@app.errorhandler(500)
def internal_error(error):

    return render_template('index.html', jump_div='rep-input', error_msg='Please enter a full address below.')

def get_reps(officials, offices, divisions):
	reps = [];

	social_icon_lookup = {
		'YouTube': 'youtube',
		'Facebook': 'facebook',
		'Twitter': 'twitter',
		'GooglePlus': 'google-plus'
		};

	social_link_lookup = {
	    'YouTube': 'https://www.youtube.com/user/',
	    'Facebook': 'https://www.facebook.com/',
	    'Twitter': 'https://twitter.com/',
	    'GooglePlus': 'https://plus.google.com/'
	};

	print(divisions);


	for division in divisions:
		if divisions[division].get('officeIndices') != None:
			for office in divisions[division]['officeIndices']:
				print(office);
				office_name = offices[office];

				print(offices[office]['officialIndices']);

				for official in offices[office]['officialIndices']:
					print(official)
					rep = {
						'person': None,
						'name': None,
						'office': office_name['name'],
						'address': None,
						'party': None,
						'photoUrl': None,
						'phones': None,
						'urls': None,
						'channels': None,
						'officeIndex': None
					}

					person = officials[official];
					print(person);
					rep['person'] = person;
					rep['name'] = person['name'];
					rep['party'] = person['party'];
					rep['officeIndex'] = office;
					if person.get('photoUrl'):
						rep['photoUrl'] = person['photoUrl'];

					if person.get('channels') != None:
						channels = [];
						for channel in person['channels']:
							if channel['type'] != 'GooglePlus' and channel['type'] != 'YouTube':
								channel['icon'] = social_icon_lookup[channel['type']];
								channel['link'] = social_link_lookup[channel['type']] + channel['id'];
								channels.append(channel);
	                        
					rep['channels'] = channels;

					if person.get('address') != None:
					    rep['address'] = person['address'];
					
					if person.get('phones') != None:
					    rep['phones'] = person['phones'];
					
					if person.get('urls') != None:
					    rep['urls'] = person['urls'];
					
					if person.get('emails') != None:
					    rep['emails'] = person['emails'];
					
					print(rep)

					if rep['office'] != 'President of the United States':	
						reps.append(rep)

	return reps;
