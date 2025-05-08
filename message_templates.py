# Message Templates for Reddit Bot
# This file contains different message templates and their associated keywords

# Template 1: General Activism Resources
ACTIVISM_KEYWORDS = [
    'how to help', 'get involved', 'volunteer', 'organize', 
    'protest', 'rally', 'petition', 'activism', 'activist',
    'looking for resources', 'need advice', 'where can I', 
    'how do I start', 'beginner activist'
]

ACTIVISM_TEMPLATE = """
Hello! I noticed you're interested in getting involved with activism or social justice work.

Here are some resources that might be helpful:

## Getting Started
- [Mutual Aid Hub](https://www.mutualaidhub.org/) - Find local mutual aid networks
- [Activist Handbook](https://www.activisthandbook.org/) - Comprehensive guide for activists
- [Beautiful Trouble](https://beautifultrouble.org/toolbox/) - Tactics, principles, and case studies

## Digital Security
- [Security in a Box](https://securityinabox.org/) - Digital security tools and tactics
- [Digital First Aid Kit](https://digitalfirstaid.org/) - Help for those facing digital threats

## Community Building
- [The Anarres Project](https://anarresproject.org/resources-for-organizing-and-liberation/) - Resources for organizing
- [Training for Change](https://www.trainingforchange.org/tools/) - Workshop tools and activities

I'm an automated assistant, but I hope these resources help you in your journey!

*This is an automated message. Please contact u/Massive-News-9371 with any questions about this bot.*
"""

# Template 2: Mutual Aid Resources
MUTUAL_AID_KEYWORDS = [
    'mutual aid', 'community support', 'solidarity', 'food bank',
    'resource sharing', 'community fridge', 'free store', 'aid network',
    'help neighbors', 'community care', 'direct support'
]

MUTUAL_AID_TEMPLATE = """
Hello! I noticed you're interested in mutual aid and community support networks.

Here are some resources specifically focused on mutual aid:

## Mutual Aid Networks
- [Mutual Aid Hub](https://www.mutualaidhub.org/) - Find local mutual aid networks in your area
- [Big Door Brigade](https://bigdoorbrigade.com/) - Resources on how to start mutual aid projects
- [Mutual Aid Disaster Relief](https://mutualaiddisasterrelief.org/) - Support for disaster response

## Guides & Tools
- [Mutual Aid Toolbox](https://mutualaiddisasterrelief.org/resources/) - Practical guides for organizing
- [Dean Spade's Mutual Aid Resources](https://www.deanspade.net/mutual-aid-building-solidarity-during-this-crisis-and-the-next/) - Readings and resources

## Examples & Case Studies
- [Mutual Aid NYC](https://mutualaid.nyc/resources-2/) - Example of a city-wide mutual aid network
- [Neighborhood Pods](https://pod.coop/pod-mapping-for-mutual-aid/) - How to organize neighborhood pods

I hope these resources help you build community support networks!

*This is an automated message. Please contact u/Massive-News-9371 with any questions about this bot.*
"""

# Template 3: Digital Security for Activists
SECURITY_KEYWORDS = [
    'digital security', 'online privacy', 'secure messaging', 'encryption',
    'protect data', 'surveillance', 'secure communication', 'privacy tools',
    'anonymity', 'secure browsing', 'protect identity', 'digital safety'
]

SECURITY_TEMPLATE = """
Hello! I noticed you're asking about digital security and privacy for activists.

Here are some specialized resources for staying safe online:

## Essential Security Tools
- [Security in a Box](https://securityinabox.org/) - Comprehensive digital security tools and tactics
- [EFF's Surveillance Self-Defense](https://ssd.eff.org/) - Tips, tools and how-tos for safer online communications
- [Digital First Aid Kit](https://digitalfirstaid.org/) - Help for those facing digital threats

## Secure Communication
- [Signal](https://signal.org/) - Encrypted messaging app
- [ProtonMail](https://protonmail.com/) - Encrypted email service
- [Jitsi Meet](https://meet.jit.si/) - Secure video conferencing

## Anonymity & Privacy
- [Tor Browser](https://www.torproject.org/) - Browse the web anonymously
- [Tails OS](https://tails.boum.org/) - Privacy-focused operating system
- [Privacy Tools](https://www.privacytools.io/) - Services that respect your privacy

Stay safe in your digital activism!

*This is an automated message. Please contact u/Massive-News-9371 with any questions about this bot.*
"""

# Template 4: Community Organizing Resources
ORGANIZING_KEYWORDS = [
    'community organizing', 'grassroots', 'direct action', 'campaign',
    'coalition building', 'mobilizing', 'canvassing', 'base building',
    'leadership development', 'strategy', 'movement building'
]

ORGANIZING_TEMPLATE = """
Hello! I noticed you're interested in community organizing and movement building.

Here are some resources focused on effective organizing:

## Organizing Fundamentals
- [Midwest Academy Manual](https://www.midwestacademy.com/manual/) - Classic organizing strategy guide
- [Beautiful Trouble](https://beautifultrouble.org/toolbox/) - Tactics, principles, and case studies
- [Training for Change](https://www.trainingforchange.org/tools/) - Workshop tools and activities

## Building Power
- [Movement School](https://www.movementschool.us/) - Training for grassroots organizers
- [Momentum](https://www.momentumcommunity.org/resources) - Movement building framework and resources
- [Ayni Institute](https://ayni.institute/resources/) - Social movement ecology resources

## Strategic Campaigns
- [Center for Story-based Strategy](https://www.storybasedstrategy.org/tools-and-resources) - Narrative tools for campaigns
- [The Change Agency](https://thechangeagency.org/resources/) - Campaign planning tools
- [Commons Social Change Library](https://commonslibrary.org/) - Comprehensive activist resource collection

I hope these resources help strengthen your organizing work!

*This is an automated message. Please contact u/Massive-News-9371 with any questions about this bot.*
"""

# All templates dictionary - maps keywords to templates
TEMPLATES = {
    'General Activism': {
        'keywords': ACTIVISM_KEYWORDS,
        'message': ACTIVISM_TEMPLATE,
        'description': 'General activism resources'
    },
    'Mutual Aid': {
        'keywords': MUTUAL_AID_KEYWORDS,
        'message': MUTUAL_AID_TEMPLATE,
        'description': 'Mutual aid and community support resources'
    },
    'Digital Security': {
        'keywords': SECURITY_KEYWORDS,
        'message': SECURITY_TEMPLATE,
        'description': 'Digital security and privacy resources'
    },
    'Community Organizing': {
        'keywords': ORGANIZING_KEYWORDS,
        'message': ORGANIZING_TEMPLATE,
        'description': 'Community organizing and movement building resources'
    }
}

# Functions for template management
def get_all_templates():
    """Get all available templates."""
    return [{'name': name, 'keywords': data['keywords'], 'message': data['message']} 
            for name, data in TEMPLATES.items()]

def get_template(template_name):
    """Get a specific template by name."""
    if template_name in TEMPLATES:
        return {
            'name': template_name,
            'keywords': TEMPLATES[template_name]['keywords'],
            'message': TEMPLATES[template_name]['message']
        }
    return None

def update_template(template_name, keywords, message):
    """Update an existing template."""
    if template_name in TEMPLATES:
        TEMPLATES[template_name]['keywords'] = keywords
        TEMPLATES[template_name]['message'] = message
        return True
    return False

def add_template(template_name, keywords, message):
    """Add a new template."""
    if template_name not in TEMPLATES:
        TEMPLATES[template_name] = {
            'keywords': keywords,
            'message': message,
            'description': f'Custom template: {template_name}'
        }
        return True
    return False

# Function to find the best template for a given text
def get_template_for_text(text):
    """Find the best template based on keyword matches in the text."""
    text = text.lower()
    
    # Count keyword matches for each template
    matches = {}
    for name, data in TEMPLATES.items():
        matches[name] = sum(1 for keyword in data['keywords'] if keyword.lower() in text)
    
    # Find the template with the most matches
    if matches:
        best_template = max(matches.items(), key=lambda x: x[1])
        
        # Only return a template if there's at least one match
        if best_template[1] > 0:
            template_name = best_template[0]
            return {
                'name': template_name,
                'message': TEMPLATES[template_name]['message']
            }
    
    return None
