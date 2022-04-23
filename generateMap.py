import re
import codecs


# This file is used to generate a static code file to be called by the program
def generateHtml():
    # Gets the generated html and read it to variable
    f=codecs.open("Website/templates/map.html", 'r')
    html = f.read()
    
    # Using regex to extract out the nodes
    between_script = re.search('(?<=/body>\n<script>)(.|\r|\n)*(?=</script)', html)
    map_id = re.search('(?<= var)(.*)(?= =)', html)

    home = '''    {% extends "base.html" %}

        {% block title %}Lift Ride Hailing{% endblock %}
        
        {% block userLocationInput %}        
        <form method="POST" id="testForm">
            <div class="form-row" id="formBlock">
                <div class="col">
                    <input type="text" maxlength="6" data-rule-maxlength="6" id="startingLocation" name="startingLocation" oninput="javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength); this.value = this.value.replace(/[^0-9.]/g, '').replace(/(\..*)\./g, '$1');" class="form-control" placeholder= {{ startingPostal }} />
                </div>
                <div class="col">
                    <input type="text" maxlength="6" data-rule-maxlength="6" id="endingLocation" name="endingLocation" oninput="javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength); this.value = this.value.replace(/[^0-9.]/g, '').replace(/(\..*)\./g, '$1');" class="form-control" placeholder= {{ endingPostal }} />
                </div>
                <div class="col">
                    <button type="submit" class="btn btn-primary" name="submit_button" value="changeRoute">Change Route</button>
                </div>
            </div>
        </form>
    
        {% endblock %}
        
        {% block mapContent %}
        <head>
            <script>
                L_NO_TOUCH = false;
                L_DISABLE_3D = false;
            </script>

        <script src="https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js"></script>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.css"/>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css"/>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet.awesome.rotate.min.css"/>

                <style>'''
    home2 = '''
                    #''' + map_id.group().strip() + ''' {
                        margin: 0 auto;
                        height: 100%;
                        width: 70%;
                        padding-bottom: 1%;
                    }
                </style>

    </head>'''
    home3 = f'''<body>

                <div class="folium-map" id="{map_id.group().strip()}" ></div>

    </body>
    <script>'''

    home4 = '''</script>
        {% endblock %}
        '''

    home5 = '''
    {% block confirmationSection %}<br>
        <table id="confirmationTable">
        <tr>
            <th class="header1">Pick Up Point</th>
            <th class="header1">Drop Off Location</th>
            <th class="header1">No Of Passengers</th>
            <th class="header1">Car Type</th>
            <th class="header1">Total Cost</th>
            <th class="header1"></th>
        </tr>
        
        <tr>
            <td class="data">{{ startingPostal }}</td>
            <td class="data">{{ endingPostal }}</td>
            <td class="data">{{ numOfPassengers }}</td>
            <td class="data">{{ carType }}</td>
            <td class="data">SGD {{ priceCost }}</td>
            <td class="data">
            <form method="POST" id="confirmationButton">
                <button type="submit" id="confirmButton" name="submit_button" value="confirmRoute">Book</button>
            </form>
            </td>
        </tr>
        
        
        </table>
    {% endblock %}
    '''
    # Join the new html with the nodes extracted
    home += home2 + home3 + between_script.group() + home4 + home5
    
    # Save it
    f = open("Website/templates/routeOutput.html","w")
    f.write(home)
