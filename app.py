import pygame
import player
import entity
import colors
import map
import random
import settings

'''
x == width == rect.left
y == height == rect.top
'''

class App:
    def __init__(self):
        self._running = True
        self.width = settings.WINDOW_WIDTH
        self.height = settings.WINDOW_HEIGHT
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.SCALED | pygame.RESIZABLE)
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
        self.clock.tick(settings.CLOCK_RATE)
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
                    if random.randint(1, 3) == 1:
                        self._spread_color(self.m.grid[e.loc])
                if e.age_timer > settings.AGE_LENGTH:
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
        e0 = entity.Entity(0, 0, colors.RED)
        e1 = entity.Entity(self.width-10, 0, colors.GREEN)
        e2 = entity.Entity(0, self.height-10, colors.BLUE)
        e3 = entity.Entity(self.width-10, self.height-10, colors.YELLOW)
        self.entities = [e0, e1, e2, e3]
        for e in self.entities:
            self.m.grid[e.loc].append(e)

    def _p_collides(self, p, e):
        return p.loc == e.loc
    
    def _spread_color(self, collisions):
        r, g, b = 0, 0, 0
        highest_off = 0
        mod = random.randint(1, 3)
        for e in collisions:
            highest_off = e.amnt_offspring if e.amnt_offspring > highest_off else highest_off
            r += e.color.r
            # if r <= 100:
            #     r = r+75 if mod == 1 else r+50
            g += e.color.g
            # if g <= 100:
            #     g = g+75 if mod == 2 else g+50
            b += e.color.b
            # if b <= 100:
            #     b = b+75 if mod == 3 else b+50
        #print(str(int(r/len(collisions))) + " " + str(int(g/len(collisions))) + " " + str(int(b/len(collisions))))
        c = pygame.Color(int(r/len(collisions)), int(g/len(collisions)), int(b/len(collisions)))
        for e in collisions:
            if e.amnt_offspring < highest_off:
                e.color = c
    
    def _spread_disease(self, collisions):
        for e in collisions:
            if not e.diseased and random.randint(1, 2) == 1:
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
        elif key == 'r':
            for e in entities:
                e.color = pygame.Color(random.randint(10, 200), random.randint(10, 200), random.randint(10, 200))
        elif key == '1':
            for e in entities:
                e.color = colors.RED
        elif key == '2':
            for e in entities:
                e.color = colors.GREEN
        elif key == '3':
            for e in entities:
                e.color = colors.BLUE
        elif key == '4':
            for e in entities:
                e.color = colors.YELLOW
        elif key == '5':
            for e in entities:
                e.color = colors.PURPLE
        elif key == 'c':
            for e in entities:
                r_cpy, g_cpy, b_cpy = e.color.r, e.color.g, e.color.b
                e.color.r = g_cpy
                e.color.g = b_cpy
                e.color.b = r_cpy
        elif key == 'f':
            for e in entities:
                e.color.r = 255 - e.color.r
                e.color.g = 255 - e.color.g
                e.color.b = 255 - e.color.b
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