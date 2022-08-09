try:
    import time

    import displayio
    import adafruit_imageload

    from general import buttons
    from general import group

    from pacman import pacman_himself
    from pacman import pacman_map
    from pacman import cheese_logic
    from pacman import score
    from pacman import announcement
    from pacman import ghosts

    HEIGHT = 160
    WIDTH = 128

    # Selection of maps and character
    pacman_character_sprites = "/pacman/pacman_himself_sprites.bmp"
    pacman_map_sprites = "/pacman/pacman_map1.bmp"
    pacman_cheese_sprites = "/pacman/cheese_n_stuff.bmp"
    pacman_score_sprites = "/pacman/scoreboard.bmp"
    announcer_text = "/pacman/announcements.bmp"

    # ghosts
    ghost1_sprite = "/pacman/ghost_clyde.bmp"
    ghost2_sprite = "/pacman/ghost_greeny.bmp"
    ghost3_sprite = "/pacman/ghost_marge.bmp"

    # Setup
    button_pad = buttons.Buttons(BTN_X, BTN_Y, BTN_A, BTN_B)
    highscore = score.Score(pacman_score_sprites)
    chosen_map = pacman_map.PacmanMap(pacman_map_sprites)
    pacman_character = pacman_himself.PacmanHimself(
        pacman_character_sprites, chosen_map, WIDTH, HEIGHT)
    cheese = cheese_logic.Cheese(pacman_cheese_sprites, pacman_character, highscore, pacman_map.cheese_map1)
    announcer = announcement.Announcer(announcer_text)
    ghost1 = ghosts.Ghost(ghost1_sprite, chosen_map,
        pacman_character, highscore, WIDTH, HEIGHT,
        2,WIDTH//2 - 21, HEIGHT//2 - 7, 1
    )
    ghost2 = ghosts.Ghost(ghost2_sprite, chosen_map,
        pacman_character, highscore, WIDTH, HEIGHT,
        1, WIDTH//2 - 7, HEIGHT//2 - 7, 1
    )
    ghost3 = ghosts.Ghost(ghost3_sprite, chosen_map,
        pacman_character, highscore, WIDTH, HEIGHT,
        0, WIDTH//2 + 8, HEIGHT//2 - 7, 1
    )

    ghosts = [ghost1, ghost2, ghost3]

    # Make group
    pacman_group = group.Group(
        chosen_map.sprite,
        cheese.sprite,
        pacman_character.sprite,
        announcer.group,
    )

    display.show(pacman_group.group)

    announcer.start()
    pacman_group.group.pop()
    pacman_group.append(ghost1.sprite, ghost2.sprite, ghost3.sprite)
    pacman_group.append(highscore.score_group, announcer.group)

    # Game loop
    while True:
        button_value = button_pad.get_value()
        pacman_character.move(button_value)

        cheese.update()

        if cheese.check_victory():
            announcer.victory()

        for ghost in ghosts:
            if ghost.check_collision():
                pacman_character.dead()
                announcer.dead()
                break

        if not pacman_character.alive:
            break

        for ghost in ghosts:
            ghost.move()

        # Update time
        time.sleep(0.01)


except Exception as ex:
    print(ex)
    for ghost in ghosts:
        print(ghost.sprite.x, ghost.sprite.y, ghost.x_position, ghost.y_position)
    print(pacman_character.sprite.x, pacman_character.sprite.y, pacman_character.x_position, pacman_character.y_position)

