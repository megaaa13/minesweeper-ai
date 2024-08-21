import pygame
from action import Action
from agent import Agent
import signal

class HumanAgent(Agent):
    def __init__(self):
        self.clock = pygame.time.Clock()

    def get_action(self, state) -> Action:
        action = None
        while not action:
            self.clock.tick(30)
            for event in pygame.event.get():
                # Check if player close window
                if event.type == pygame.QUIT:
                    action = Action("Exit", None)
                # Check if play restart
                if state.getStatus() == "Game Over" or state.getStatus() == "Win":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            action = Action("Restart", None)
                            print("Restart")
                else:
                    if event.type == pygame.MOUSEBUTTONUP:
                        print(event.pos)
                        for i in state.getGrid():
                            for j in i:
                                if j.rect.collidepoint(event.pos):
                                    if event.button == 1:
                                        # If the player left clicked
                                        action = Action("Reveal", j)
                                        break
                                    elif event.button == 3:
                                        # If the player right clicked
                                        action = Action("Flag", j)
                                        break
        return action

    
    def get_name(self):
        return "Human Agent"