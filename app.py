import pygame
import player
import entity
import colors

class App:
    def __init__(self):
        self._running = True
        self.height = 480
        self.width = 360
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.height, self.width))
        self.p = player.Player(self.height/2, 0)
        self.entities = []
        self.total_ent = len(self.entities)
        self.keys = []
        self.dir_timer = 0
        self.move_timer = 0
    
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
        if len(self.entities) == 0:
            self._running = False
        self.clock.tick(15)
        self.p.rect = self._handlekey(self.keys, self.p.rect)

        for e in self.entities:
            e.dir_timer += self.clock.get_time()
            e.move_timer += self.clock.get_time()
            e.update(self.height, self.width)
    
    def on_render(self):
        self.screen.fill(colors.WHITE)
        pygame.draw.rect(self.screen, colors.RED, self.p.rect)
        for e in self.entities:
            if self._p_collides(self.p.rect, e.rect) or e.age == e.age_limit:
                self.entities.remove(e)
                self._obituary(e)
            else:
                pygame.draw.rect(self.screen, e.color, e.rect)
                if e.age_timer > 3400:
                    e.age += 1
                    offspring = e.reproduce()
                    if offspring:
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
        e0 = entity.Entity(self.height/2, self.width/2)
        self.entities.append(e0)

    def _p_collides(self, rect1, rect2):
        return abs(rect1.left - rect2.left) < 10 and abs(rect1.top - rect2.top) < 10

    def _obituary(self, e):
        print("an entity of generation " + str(e.generation) + " has perished after " + str(e.age) + " ages, leaving " + str(e.amnt_offspring) + " offspring")

    def _handlecmd(self, key, entities):
        if key == 'x':
            for i in range(int(len(entities)/2)):
                self._obituary(entities[i])
                entities.pop(i)
        elif key == 'q':
            self._running = False

    def _handlekey(self, keys, rect):
        res = rect.copy()
        if 'w' in keys and rect.top != 0:
            res = res.move(0, -10)
        if 'a' in keys and rect.left != 0:
            res = res.move(-10, 0)
        if 's' in keys and rect.bottom != self.width:
            res = res.move(0, 10)
        if 'd' in keys and rect.right != self.height:
            res = res.move(10, 0)
        return res