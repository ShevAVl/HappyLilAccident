# "HappyLilAccident"  
A discord bot prototype for the *"Attic Dwellers"* server

## Dependencies
language - python 3.10 
modules - in dependencies.txt  
to install the modules: pip install -r dependencies.txt

## File dependencies (files that the bot won't launch without)
**tldr**:  
To make things work do the following:
<ul>
  <li>
    create a .env file with a BOT_TOKEN = <token> item
  </li>
  <li>
    remove the "_example" part of json/privilegedUsers.json
  </li>
  <li>
    remove the "_example" part from CommonData_example.db
  </li>
  <li>
    put the included libsteam_api.so file into /usr/lib directory and enter these commands:  
  </li>
    <ul>
      <li>
        chmod 0755 /usr/lib/libsteam_api.so - to give the lib the necessary privileges
      </li>
      <li>
        ldconfig - updating the lib cache
      </li>
    </ul>
  </li>
</ul>
The list of the files required for successful launch is stored in json/essentialFiles (essentialFiles.json itself is also an essential file)   
Here are brief descriptions of those files:  
<ul>
  <li>
    .env - only needs to contain a single item: BOT_TOKEN = <token>. You'll have to create this one yourself
  </li>
  <li>
    CommonData.db - includes some  miscellaneous data. Could easily be removed at this point, but it'll get more important farther into the development the bot is
  </li>
    cogs.json - lists currently varified cog-extension for the bot (cog-files store bot's commands and event managers)
  <li>
    commandList.json - a list of currently available bot commands, used to output the list as a part of the "$info" command
  </li>
  <li>
    privilegedUsers.json - list of IDs of users who're allowed to use certain commands (atm it's only "$setm308") that edit backend data in any way
  </li>
  <li>
    PDTracker - an executable that connects to a running Steam client and retrievs a list of active PDTH lobbies
  </li>
  <li>
    steam_appid.txt - contains an appID of PDTH (necessary for PDTracker)
  </li>
</ul>
Note that some of these files are present in this repo with an "_example* suffix. It means that these files don't contain any valid data and you will have to edit them yourself if you want the corresponding functions to work properly. Nevertheless, if you just remove the "_example" part, the bot will work just fine, although some functions will not do what they are supposed to do.
_example files:
<ul>
  <li>
    json/privilegedUsers_example.json - has a placeholder userID that doesn't belong to any real user. Without custom editing command "$setm308" will do nothing
  </li>
  <li>
    CommonData.db - has a placeholder userID for the "on_message* event. Without editing the "userid_cz" field event "on_message" will do nothing
  </li>
</ul>

## Command list
<ol>
  <li>
    $info - outputs a list of available bot commands
  </li>
  <li>
     $vote - starts a "vote" consisting of a topic in bold and options separated with ">"  
     Does not include a feature to "summarize the results"
  </li>
  <li>
     $voteinfo - in-depth explanation on how to use $vote, with an example
  </li>
  <li>
     $m308 - outputs the amount of times a certain server member mentions a pattern "m308" on public channels\threads
  </li>
  <li>
     $setm308 - allows specified users to set the counter used in $m308 to any number in range of [0, 2^64 - 1]
  </li>
  <li>
    $pdth - attempts to fetch active PDTH lobbies and, if successful, creates a thread after the command call and outputs the lobby info in there
  </li>
  <li>
    $gen - generates a number in a [1,100] range and sends a message containing it right after the command call
  </li>
</ol>

## Credits
  [Liquor](https://steamcommunity.com/id/SoyFood) - the creator  
  [P0wderGang3r](https://steamcommunity.com/id/P0wderGang3r) - general feedback, code reviews and ideas  
  [cz](https://steamcommunity.com/id/cz731)  -  goofball, ideas  
  [!nfern](https://steamcommunity.com/id/folwboiard) -  server owner, ideas  
  [zneix](https://steamcommunity.com/id/zneix) - linux/git support, ideas
