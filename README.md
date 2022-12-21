<h1>Pygame Simulation</h1>
<h2>Overview</h2>
<p>
Simulates the life and behavior of small colored squares called entities. Entities can move around at random, interact with other entities and reproduce to build colonies that share 'genetic' characteristics (mostly just color). Unfortunately, to control the population of these entities, disease also has a small chance to mutate in offspring which will spread by contact. Any entity that has contracted a disease will be unable to reproduce. Ultimately the entities will live, spread, and die while creating interesting patterns/color palettes in a pseudo-biological way. It is also possible to control a player entity which is bright red and deletes any entity on contact; but why would you want to do that? The player entity is disabled by default. Nothing in this project is scientific. I made it all up.
</p>
<h2>Commands</h2>
<b>q</b>: quit and exit the program</br>
<b>w, a, s, d</b>: move player entity (if present)</br>
<b>1, 2, 3, 4, 5</b>: change all entities to Red, Green, Blue, Yellow, or Purple respectively</br>
<b>r</b>: randomize all entity colors</br>
<b>c</b>: shift entity colors by one position (red values become green value, green becomes blue...)</br>
<b>f</b>: invert all entity colors</br>
<b>x</b>: delete half of all entities</br>