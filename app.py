import pygame
import player
import entity
import colors
import map

'''
x == width == rect.left
y == height == rect.top
'''

class App:
    def __init__(self):
        self._running = True
        self.width = 640
        self.height = 480
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        # self.p = player.Player(int(self.width/2), 0)
        self.p = player.Player(1000, 1000)
        self.entities = []
        self.total_ent = len(self.entities)
        self.keys = []
        self.dir_timer = 0
        self.move_timer = 0
        self.m = map.Map(self.width, self.height)
    
    def on_init(self):
        pygame.init()
        self._build_entities()
        self._running = True
    
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYUP:
            self.keys.remove(event.unicode)
        if event.type == pygame.KEYDOWN:
            self._handlecmd(event.unicode, self.entities)
            self.keys.append(event.unicode)

    def on_loop(self):
        # if len(self.entities) == 0:
        #     self._running = False
        self.clock.tick(30)
        self.p.rect = self._handlekey(self.keys, self.p.rect)

        for e in self.entities:
            e.dir_timer += self.clock.get_time()
            e.move_timer += self.clock.get_time()
            self.m.grid[e.loc].remove(e)
            e.update(self.width, self.height)
            self.m.grid[e.loc].append(e)
    
    def on_render(self):
        self.screen.fill(colors.WHITE)
        pygame.draw.rect(self.screen, colors.RED, self.p.rect)
        for e in self.entities:
            if self._p_collides(self.p, e) or e.age >= e.age_limit:
                self.m.grid[e.loc].remove(e)
                self.entities.remove(e)
                self._obituary(e)
            else:
                pygame.draw.rect(self.screen, e.color, e.rect)
                if len(self.m.grid[e.loc]) > 1:
                    if e.diseased:
                        self._spread_disease(self.m.grid[e.loc])
                    #self._spread_color(self.m.grid[e.loc])
                if e.age_timer > 3400:
                    e.age += 1
                    offspring = e.reproduce()
                    if offspring:
                        self.m.grid[offspring.loc].append(offspring)
                        self.entities.append(offspring)
                        self.total_ent += 1
                    e.age_timer = 0
                else:
                    e.age_timer += self.clock.get_time()
        pygame.display.flip()

    def on_cleanup(self):
        print("total entities: " + str(self.total_ent))
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
    
    # helpers
    def _build_entities(self):
        e0 = entity.Entity(int(self.width/2), int(self.height/2))
        self.m.grid[e0.loc].append(e0)
        self.entities.append(e0)

    def _p_collides(self, p, e):
        return p.loc == e.loc
    
    # def _spread_color(self, collisions):
    #     r, g, b = 0, 0, 0
    #     for e in collisions:
    #         r += e.color.r
    #         g += e.color.g
    #         b += e.color.b
    #     print(str(int(r/3)) + " " + str(int(g/3)) + " " + str(int(b/3)))
    #     c = pygame.Color(int(r/3), int(g/3), int(b/3))
    #     for e in collisions:
    #         e.color = c
    
    def _spread_disease(self, collisions):
        for e in collisions:
            if not e.diseased:
                e.diseased = True

    def _obituary(self, e):
        if e.diseased:
            print("an entity of generation " + str(e.generation) + " has perished from disease after " + str(e.age) + " ages, leaving " + str(e.amnt_offspring) + " offspring")
        else:
            print("an entity of generation " + str(e.generation) + " has perished after " + str(e.age) + " ages, leaving " + str(e.amnt_offspring) + " offspring")

    def _handlecmd(self, key, entities):
        if key == 'x':
            for i in range(int(len(entities)/2)):
                self._obituary(entities[i])
                self.m.grid[entities[i].loc].remove(entities[i])
                entities.pop(i)
        elif key == 'q':
            self._running = False

    def _handlekey(self, keys, rect):
        res = rect.copy()
        if 'w' in keys and rect.top != 0:
            res = res.move(0, -10)
        if 'a' in keys and rect.left != 0:
            res = res.move(-10, 0)
        if 's' in keys and rect.bottom != self.height:
            res = res.move(0, 10)
        if 'd' in keys and rect.right != self.width:
            res = res.move(10, 0)
        self.p.loc = (res.left, res.top)
        return res