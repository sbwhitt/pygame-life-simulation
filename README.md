<h1>Pygame Simulation</h1>

<h2>Overview</h2>

<p>
Simulates the life and behavior of small colored squares called entities. Entities can move around at random, interact with other entities and reproduce to build colonies that share 'genetic' characteristics (mostly just color). Unfortunately, to control the population of these entities, disease also has a small chance to mutate in offspring which will spread by contact. Any entity that has contracted a disease will be unable to reproduce. They also have a tendency to eat one another. Ultimately the entities will live, spread, and die while creating interesting patterns/color palettes in a pseudo-biological way. Nothing in this project is scientific. I made it all up.
</p>

<h2>Commands</h2>

<b>esc</b>: pause program</br>
<b>del</b>: delete selected entities</br>
<b>left click</b>: drag to select, create, or delete entities</br>
<b>middle click</b>: place entities of selected color extending outward</br>
<b>right click</b>: drag screen</br>
<b>1, 2, 3, 4, 5, 6</b>: change selected entities to Red, Green, Blue, Yellow, Purple, or Cyan respectively</br>
<b>ctrl+a</b>: select all entities</br>
<b>ctrl+s</b>: save current game state to a .ent save file (located in saves directory)</br>
<b>q</b>: quit and exit the program</br>
<b>r</b>: randomize selected entity colors</br>
<b>c</b>: shift selected entity colors by one position (red values become green value, green becomes blue...)</br>
<b>f</b>: invert selected entity colors</br>
<b>x</b>: delete half of all entities</br>
<b>e</b>: add six entities of each color to edges of screen</br>
<b>d</b>: toggle whether diseased entities will be marked or not</br>
<b>l</b>: toggle logging</br>
<b>h</b>: toggle colony highlighting</br>
<b>p</b>: toggle side panel</br>
<b>b</b>: toggle bottom panel</br>

<h2>Building</h2>
Requires <a href="https://www.pygame.org/wiki/GettingStarted" target="_blank">pygame</a> to run.</br>
Then simply clone and run:
<code>python main.py</code></br>
Or, if trying to load a save file, run: <code>python main.py (file-name).ent</code>

<h2>Screenshots</h2>

<b>Current examples:</b></br>
<img src="./imgs/current.PNG"/></br>
</br>
<img src="./imgs/current1.PNG"/></br>
</br>
<b>Old example screenshots:</b></br>
<img src="./imgs/exampleOLD.PNG"/></br>
</br>
<img src="./imgs/example2OLD.PNG"/></br>
</br>
<b>Old simulation example after a long time:</b></br>
<img src="./imgs/exampleLONG_OLD.PNG"/></br>
