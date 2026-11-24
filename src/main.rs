use macroquad::prelude::*;

const WORLD_W: f32 = 1200.0;
const FLOOR_Y: f32 = 207.0;
const VIEW_W: f32 = 480.0;
const VIEW_H: f32 = 270.0;

struct Actor {
    x: f32,
    y: f32,
    vx: f32,
    vy: f32,
}

struct Enemy {
    x: f32,
    y: f32,
    kind: u8, // 0 = street punk, 1 = brawler, 2 = demon samurai boss
    hp: i32,
    alive: bool,
    vx: f32,
    attack_cd: f32,
    attack_timer: f32,
    hit_timer: f32,
    death_timer: f32,
}

impl Enemy {
    fn new(x: f32, kind: u8, hp: i32) -> Self {
        Self {
            x,
            y: FLOOR_Y - 29.0,
            kind,
            hp,
            alive: true,
            vx: 0.0,
            attack_cd: 0.0,
            attack_timer: 0.0,
            hit_timer: 0.0,
            death_timer: 0.0,
        }
    }
}

struct Projectile {
    x: f32,
    y: f32,
    vx: f32,
    alive: bool,
}

struct Game {
    player: Actor,
    enemies: Vec<Enemy>,
    projectiles: Vec<Projectile>,
    camera: f32,
    hp: i32,
    kills: i32,
    elapsed: f32,
    slash: f32,
    combo: usize,
    throw_timer: f32,
    throw_cd: f32,
    dash_timer: f32,
    dash_cd: f32,
    player_hurt_timer: f32,
    invuln: f32,
    facing: f32,
    won: bool,
    dead: bool,
    death_time: f32,
}

impl Game {
    fn new() -> Self {
        Self {
            player: Actor { x: 82.0, y: FLOOR_Y - 29.0, vx: 0.0, vy: 0.0 },
            enemies: vec![
                Enemy::new(340.0, 0, 1),
                Enemy::new(570.0, 1, 2),
                Enemy::new(810.0, 0, 1),
                Enemy::new(1030.0, 2, 6),
            ],
            projectiles: Vec::new(),
            camera: 0.0,
            hp: 3,
            kills: 0,
            elapsed: 0.0,
            slash: 0.0,
            combo: 2,
            throw_timer: 0.0,
            throw_cd: 0.0,
            dash_timer: 0.0,
            dash_cd: 0.0,
            player_hurt_timer: 0.0,
            invuln: 0.0,
            facing: 1.0,
            won: false,
            dead: false,
            death_time: 0.0,
        }
    }

    fn reset(&mut self) {
        *self = Self::new();
    }

    fn damage_player(&mut self) {
        if self.invuln > 0.0 || self.dead {
            return;
        }
        self.hp -= 1;
        self.invuln = 0.82;
        self.player_hurt_timer = 0.32;
        if self.hp <= 0 {
            self.dead = true;
            self.death_time = 0.0;
        }
    }

    fn damage_enemy(&mut self, index: usize) {
        if index >= self.enemies.len() || !self.enemies[index].alive {
            return;
        }
        let enemy = &mut self.enemies[index];
        enemy.hp -= 1;
        enemy.hit_timer = 0.22;
        if enemy.hp <= 0 {
            enemy.alive = false;
            enemy.death_timer = if enemy.kind == 2 { 0.82 } else { 0.42 };
            self.kills += 1;
        }
    }

    fn update(
        &mut self,
        dt: f32,
        left: bool,
        right: bool,
        jump: bool,
        attack: bool,
        dash: bool,
        slow: bool,
        throw_shuriken: bool,
    ) {
        self.elapsed += dt;
        if self.dead {
            self.death_time += dt;
            return;
        }
        if self.won {
            return;
        }

        let step = if slow { dt * 0.42 } else { dt };
        self.slash = (self.slash - step).max(0.0);
        self.throw_timer = (self.throw_timer - step).max(0.0);
        self.throw_cd = (self.throw_cd - step).max(0.0);
        self.dash_timer = (self.dash_timer - step).max(0.0);
        self.dash_cd = (self.dash_cd - step).max(0.0);
        self.player_hurt_timer = (self.player_hurt_timer - step).max(0.0);
        self.invuln = (self.invuln - step).max(0.0);

        let dir = (right as i32 - left as i32) as f32;
        if dir != 0.0 {
            self.facing = dir.signum();
        }
        self.player.vx = dir * 158.0;

        if dash && self.dash_cd <= 0.0 {
            self.dash_timer = 0.20;
            self.dash_cd = 0.78;
            self.player.vx = self.facing * 410.0;
            for i in 0..self.enemies.len() {
                if self.enemies[i].alive
                    && (self.enemies[i].x - self.player.x).abs() < 66.0
                    && (self.enemies[i].y - self.player.y).abs() < 52.0
                {
                    self.damage_enemy(i);
                }
            }
        }

        if jump && self.player.vy.abs() < 1.0 {
            self.player.vy = -302.0;
        }
        self.player.vy = (self.player.vy + 760.0 * step).min(430.0);
        self.player.x = (self.player.x + self.player.vx * step).clamp(0.0, WORLD_W - 24.0);
        self.player.y += self.player.vy * step;

        if self.player.y + 29.0 >= FLOOR_Y && self.player.vy >= 0.0 {
            self.player.y = FLOOR_Y - 29.0;
            self.player.vy = 0.0;
        }
        if self.player.y > 310.0 {
            self.damage_player();
            self.player.x = (self.player.x - 90.0).max(30.0);
            self.player.y = FLOOR_Y - 29.0;
            self.player.vy = 0.0;
        }

        if attack && self.slash <= 0.0 {
            self.slash = 0.34;
            self.combo = (self.combo + 1) % 3;
            let mut hits = Vec::new();
            for (i, enemy) in self.enemies.iter().enumerate() {
                let dx = (enemy.x - self.player.x) * self.facing;
                if enemy.alive
                    && dx >= -8.0
                    && dx <= 112.0
                    && (enemy.y - self.player.y).abs() < 58.0
                {
                    hits.push(i);
                }
            }
            for i in hits {
                self.damage_enemy(i);
            }
        }

        if throw_shuriken && self.throw_cd <= 0.0 {
            self.throw_timer = 0.40;
            self.throw_cd = 0.72;
            self.projectiles.push(Projectile {
                x: self.player.x + self.facing * 25.0,
                y: self.player.y + 10.0,
                vx: self.facing * 420.0,
                alive: true,
            });
        }

        let mut player_hit = false;
        for enemy in &mut self.enemies {
            enemy.attack_cd = (enemy.attack_cd - step).max(0.0);
            enemy.attack_timer = (enemy.attack_timer - step).max(0.0);
            enemy.hit_timer = (enemy.hit_timer - step).max(0.0);

            if !enemy.alive {
                enemy.death_timer = (enemy.death_timer - step).max(0.0);
                continue;
            }

            let dx = self.player.x - enemy.x;
            let reach = if enemy.kind == 2 { 225.0 } else { 185.0 };
            let speed = match enemy.kind { 1 => 46.0, 2 => 38.0, _ => 36.0 };
            if dx.abs() < reach {
                if dx.abs() > 36.0 {
                    enemy.vx = dx.signum() * speed;
                    enemy.x = (enemy.x + enemy.vx * step).clamp(20.0, WORLD_W - 20.0);
                } else {
                    enemy.vx = 0.0;
                    if enemy.attack_cd <= 0.0 {
                        enemy.attack_cd = if enemy.kind == 2 { 0.68 } else { 0.92 };
                        enemy.attack_timer = if enemy.kind == 2 { 0.34 } else { 0.26 };
                        if self.invuln <= 0.0 {
                            player_hit = true;
                        }
                    }
                }
            } else {
                enemy.vx = 0.0;
            }
        }
        if player_hit {
            self.damage_player();
        }

        let mut projectile_kills = Vec::new();
        for p in &mut self.projectiles {
            if !p.alive {
                continue;
            }
            p.x += p.vx * step;
            if p.x < 0.0 || p.x > WORLD_W {
                p.alive = false;
                continue;
            }
            for (i, enemy) in self.enemies.iter_mut().enumerate() {
                if enemy.alive
                    && (enemy.x - p.x).abs() < 23.0
                    && (enemy.y - p.y).abs() < 48.0
                {
                    enemy.hp -= 1;
                    enemy.hit_timer = 0.22;
                    if enemy.hp <= 0 {
                        enemy.alive = false;
                        enemy.death_timer = if enemy.kind == 2 { 0.82 } else { 0.42 };
                        projectile_kills.push(i);
                    }
                    p.alive = false;
                    break;
                }
            }
        }
        self.kills += projectile_kills.len() as i32;
        self.projectiles.retain(|p| p.alive);

        self.camera = (self.player.x - 160.0).clamp(0.0, WORLD_W - VIEW_W);
        if self.player.x > WORLD_W - 55.0 && self.enemies.iter().all(|e| !e.alive) {
            self.won = true;
        }
    }
}

struct Assets {
    city: Texture2D,
    player_idle: Texture2D,
    player_run: Texture2D,
    player_attack_1: Texture2D,
    player_attack_2: Texture2D,
    player_attack_3: Texture2D,
    player_air_attack: Texture2D,
    player_jump_start: Texture2D,
    player_jump_fall: Texture2D,
    player_dash: Texture2D,
    player_hurt: Texture2D,
    player_death: Texture2D,
    player_throw: Texture2D,
    shuriken: Texture2D,
    punk_idle: Texture2D,
    punk_walk: Texture2D,
    punk_punch: Texture2D,
    punk_hurt: Texture2D,
    brawler_idle: Texture2D,
    brawler_walk: Texture2D,
    brawler_kick: Texture2D,
    brawler_hurt: Texture2D,
    boss_idle: Texture2D,
    boss_run: Texture2D,
    boss_attack_1: Texture2D,
    boss_attack_2: Texture2D,
    boss_hurt: Texture2D,
    boss_death: Texture2D,
}

async fn load_assets() -> Assets {
    let load = |name: &str| async move {
        load_texture(name).await.unwrap_or_else(|e| panic!("Failed to load {}: {}", name, e))
    };
    let assets = Assets {
        city: load("city_stage.png").await,
        player_idle: load("player_idle.png").await,
        player_run: load("player_run.png").await,
        player_attack_1: load("player_attack_1.png").await,
        player_attack_2: load("player_attack_2.png").await,
        player_attack_3: load("player_attack_3.png").await,
        player_air_attack: load("player_air_attack.png").await,
        player_jump_start: load("player_jump_start.png").await,
        player_jump_fall: load("player_jump_fall.png").await,
        player_dash: load("player_dash.png").await,
        player_hurt: load("player_hurt.png").await,
        player_death: load("player_death.png").await,
        player_throw: load("player_throw.png").await,
        shuriken: load("player_shuriken.png").await,
        punk_idle: load("enemy_punk_idle.png").await,
        punk_walk: load("enemy_punk_walk.png").await,
        punk_punch: load("enemy_punk_punch.png").await,
        punk_hurt: load("enemy_punk_hurt.png").await,
        brawler_idle: load("enemy_brawler_idle.png").await,
        brawler_walk: load("enemy_brawler_walk.png").await,
        brawler_kick: load("enemy_brawler_kick.png").await,
        brawler_hurt: load("enemy_brawler_hurt.png").await,
        boss_idle: load("boss_idle.png").await,
        boss_run: load("boss_run.png").await,
        boss_attack_1: load("boss_attack_1.png").await,
        boss_attack_2: load("boss_attack_2.png").await,
        boss_hurt: load("boss_hurt.png").await,
        boss_death: load("boss_death.png").await,
    };
    for t in [
        &assets.city,
        &assets.player_idle, &assets.player_run,
        &assets.player_attack_1, &assets.player_attack_2, &assets.player_attack_3,
        &assets.player_air_attack, &assets.player_jump_start, &assets.player_jump_fall,
        &assets.player_dash, &assets.player_hurt, &assets.player_death, &assets.player_throw,
        &assets.shuriken,
        &assets.punk_idle, &assets.punk_walk, &assets.punk_punch, &assets.punk_hurt,
        &assets.brawler_idle, &assets.brawler_walk, &assets.brawler_kick, &assets.brawler_hurt,
        &assets.boss_idle, &assets.boss_run, &assets.boss_attack_1, &assets.boss_attack_2,
        &assets.boss_hurt, &assets.boss_death,
    ] {
        t.set_filter(FilterMode::Nearest);
    }
    assets
}

fn frame_at(time: f32, fps: f32, count: usize) -> usize {
    if count <= 1 { 0 } else { ((time.max(0.0) * fps) as usize) % count }
}

fn draw_frame(
    tex: &Texture2D,
    frame: usize,
    count: usize,
    frame_w: f32,
    frame_h: f32,
    center_x: f32,
    feet_y: f32,
    dest_w: f32,
    dest_h: f32,
    flip_x: bool,
    tint: Color,
) {
    let f = if count == 0 { 0 } else { frame.min(count - 1) };
    let src = Rect::new(f as f32 * frame_w, 0.0, frame_w, frame_h);
    let top = feet_y - dest_h * 0.94;
    draw_texture_ex(
        tex,
        center_x - dest_w * 0.5,
        top,
        tint,
        DrawTextureParams {
            dest_size: Some(vec2(dest_w, dest_h)),
            source: Some(src),
            flip_x,
            ..Default::default()
        },
    );
}

fn draw_player(game: &Game, assets: &Assets) {
    let p = &game.player;
    let feet_y = p.y + 29.0;
    let flip = game.facing < 0.0;
    let draw_w = 120.0;
    let draw_h = 120.0;

    if game.dead {
        let f = ((game.death_time * 8.0) as usize).min(4);
        draw_frame(&assets.player_death, f, 5, 96.0, 96.0, p.x, feet_y, draw_w, draw_h, flip, WHITE);
        return;
    }
    if game.player_hurt_timer > 0.0 {
        let f = frame_at(0.32 - game.player_hurt_timer, 10.0, 3);
        draw_frame(&assets.player_hurt, f, 3, 96.0, 96.0, p.x, feet_y, draw_w, draw_h, flip, WHITE);
        return;
    }
    if game.throw_timer > 0.0 {
        let f = frame_at(0.40 - game.throw_timer, 18.0, 7);
        draw_frame(&assets.player_throw, f, 7, 96.0, 96.0, p.x, feet_y, draw_w, draw_h, flip, WHITE);
        return;
    }
    if game.slash > 0.0 {
        let elapsed = 0.34 - game.slash;
        if p.vy.abs() > 10.0 {
            let f = frame_at(elapsed, 25.0, 10);
            draw_frame(&assets.player_air_attack, f, 10, 96.0, 96.0, p.x, feet_y, draw_w, draw_h, flip, WHITE);
        } else {
            let (tex, count) = match game.combo {
                0 => (&assets.player_attack_1, 7),
                1 => (&assets.player_attack_2, 7),
                _ => (&assets.player_attack_3, 6),
            };
            let f = frame_at(elapsed, 20.0, count);
            draw_frame(tex, f, count, 96.0, 96.0, p.x, feet_y, draw_w, draw_h, flip, WHITE);
        }
        return;
    }
    if game.dash_timer > 0.0 {
        let f = frame_at(0.20 - game.dash_timer, 30.0, 7);
        draw_frame(&assets.player_dash, f, 7, 96.0, 96.0, p.x, feet_y, draw_w, draw_h, flip, WHITE);
        return;
    }
    if p.vy < -10.0 {
        let f = frame_at(game.elapsed, 12.0, 3);
        draw_frame(&assets.player_jump_start, f, 3, 96.0, 96.0, p.x, feet_y, draw_w, draw_h, flip, WHITE);
    } else if p.vy > 10.0 {
        draw_frame(&assets.player_jump_fall, 0, 1, 96.0, 96.0, p.x, feet_y, draw_w, draw_h, flip, WHITE);
    } else if p.vx.abs() > 1.0 {
        let f = frame_at(game.elapsed, 16.0, 16);
        draw_frame(&assets.player_run, f, 16, 96.0, 96.0, p.x, feet_y, draw_w, draw_h, flip, WHITE);
    } else {
        let f = frame_at(game.elapsed, 8.0, 10);
        draw_frame(&assets.player_idle, f, 10, 96.0, 96.0, p.x, feet_y, draw_w, draw_h, flip, WHITE);
    }
}

fn draw_enemy(enemy: &Enemy, game: &Game, assets: &Assets) {
    if !enemy.alive && enemy.death_timer <= 0.0 {
        return;
    }
    let dx = game.player.x - enemy.x;
    let flip = dx < 0.0;
    let (center_x, feet_y) = (enemy.x, enemy.y + 29.0);

    if enemy.kind == 2 {
        let w = 142.0;
        let h = 120.0;
        if !enemy.alive {
            let progress = (0.82 - enemy.death_timer).max(0.0);
            let frame = ((progress / 0.82) * 26.0).floor().min(25.0) as usize;
            draw_frame(&assets.boss_death, frame, 26, 128.0, 108.0, center_x, feet_y, w, h, flip, WHITE);
        } else if enemy.hit_timer > 0.0 {
            let frame = frame_at(0.22 - enemy.hit_timer, 12.0, 4);
            draw_frame(&assets.boss_hurt, frame, 4, 128.0, 108.0, center_x, feet_y, w, h, flip, WHITE);
        } else if enemy.attack_timer > 0.0 {
            let frame = frame_at(0.34 - enemy.attack_timer, 20.0, 7);
            draw_frame(&assets.boss_attack_1, frame, 7, 128.0, 108.0, center_x, feet_y, w, h, flip, WHITE);
        } else if enemy.vx.abs() > 1.0 {
            let frame = frame_at(game.elapsed, 12.0, 8);
            draw_frame(&assets.boss_run, frame, 8, 128.0, 108.0, center_x, feet_y, w, h, flip, WHITE);
        } else {
            let frame = frame_at(game.elapsed, 7.0, 6);
            draw_frame(&assets.boss_idle, frame, 6, 128.0, 108.0, center_x, feet_y, w, h, flip, WHITE);
        }
        return;
    }

    let tint = if enemy.alive {
        WHITE
    } else {
        Color::from_rgba(255, 255, 255, ((enemy.death_timer / 0.42).clamp(0.0, 1.0) * 255.0) as u8)
    };
    let w = 92.0;
    let h = 92.0;
    if enemy.kind == 1 {
        if !enemy.alive || enemy.hit_timer > 0.0 {
            let frame = if enemy.alive { frame_at(0.22 - enemy.hit_timer, 10.0, 3) } else { 2 };
            draw_frame(&assets.brawler_hurt, frame, 3, 64.0, 63.0, center_x, feet_y, w, h, flip, tint);
        } else if enemy.attack_timer > 0.0 {
            let frame = frame_at(0.26 - enemy.attack_timer, 18.0, 8);
            draw_frame(&assets.brawler_kick, frame, 8, 60.0, 63.0, center_x, feet_y, w, h, flip, WHITE);
        } else if enemy.vx.abs() > 1.0 {
            let frame = frame_at(game.elapsed, 15.0, 15);
            draw_frame(&assets.brawler_walk, frame, 15, 64.0, 63.0, center_x, feet_y, w, h, flip, WHITE);
        } else {
            let frame = frame_at(game.elapsed, 7.0, 6);
            draw_frame(&assets.brawler_idle, frame, 6, 64.0, 63.0, center_x, feet_y, w, h, flip, WHITE);
        }
    } else {
        if !enemy.alive || enemy.hit_timer > 0.0 {
            let frame = if enemy.alive { frame_at(0.22 - enemy.hit_timer, 10.0, 4) } else { 3 };
            draw_frame(&assets.punk_hurt, frame, 4, 64.0, 63.0, center_x, feet_y, w, h, flip, tint);
        } else if enemy.attack_timer > 0.0 {
            let frame = frame_at(0.26 - enemy.attack_timer, 18.0, 6);
            draw_frame(&assets.punk_punch, frame, 6, 48.0, 63.0, center_x, feet_y, w, h, flip, WHITE);
        } else if enemy.vx.abs() > 1.0 {
            let frame = frame_at(game.elapsed, 12.0, 6);
            draw_frame(&assets.punk_walk, frame, 6, 64.0, 63.0, center_x, feet_y, w, h, flip, WHITE);
        } else {
            let frame = frame_at(game.elapsed, 7.0, 6);
            draw_frame(&assets.punk_idle, frame, 6, 64.0, 63.0, center_x, feet_y, w, h, flip, WHITE);
        }
    }
}

fn button(x: f32, y: f32, w: f32, h: f32, label: &str) {
    draw_rectangle(x, y, w, h, Color::from_rgba(8, 22, 43, 210));
    draw_rectangle_lines(x, y, w, h, 1.0, Color::from_rgba(31, 181, 206, 255));
    let fs = if label.len() > 3 { 8.0 } else { 17.0 };
    let d = measure_text(label, None, fs as u16, 1.0);
    draw_text(label, x + (w - d.width) / 2.0, y + h / 2.0 + fs * 0.35, fs, WHITE);
}

fn touch_state() -> (bool, bool, bool, bool, bool, bool, bool) {
    let (mut left, mut right, mut jump, mut attack, mut dash, mut slow, mut throw_shuriken) =
        (false, false, false, false, false, false, false);
    for touch in touches() {
        let x = touch.position.x * VIEW_W / screen_width();
        let y = touch.position.y * VIEW_H / screen_height();
        if x < 88.0 && y > 205.0 { left = true; }
        if (89.0..160.0).contains(&x) && y > 205.0 { right = true; }
        if (310.0..388.0).contains(&x) && y > 205.0 { jump = true; }
        if x > 388.0 && y > 205.0 { attack = true; }
        if (310.0..388.0).contains(&x) && (165.0..210.0).contains(&y) { dash = true; }
        if x > 388.0 && (165.0..210.0).contains(&y) { slow = true; }
        if x > 388.0 && (125.0..165.0).contains(&y) { throw_shuriken = true; }
    }
    (left, right, jump, attack, dash, slow, throw_shuriken)
}

#[macroquad::main("NEON BLADE")]
async fn main() {
    set_pc_assets_folder("assets");
    let assets = load_assets().await;
    let mut game = Game::new();

    loop {
        let dt = get_frame_time().min(0.033);
        let (mut left, mut right, mut jump, mut attack, mut dash, mut slow, mut throw_shuriken) = touch_state();

        left |= is_key_down(KeyCode::Left) || is_key_down(KeyCode::A);
        right |= is_key_down(KeyCode::Right) || is_key_down(KeyCode::D);
        jump |= is_key_pressed(KeyCode::Space) || is_key_pressed(KeyCode::Up);
        attack |= is_key_down(KeyCode::Z) || is_mouse_button_down(MouseButton::Left);
        dash |= is_key_down(KeyCode::V);
        slow |= is_key_down(KeyCode::X);
        throw_shuriken |= is_key_pressed(KeyCode::C);

        if (game.won || game.dead)
            && (is_mouse_button_pressed(MouseButton::Left)
                || is_key_pressed(KeyCode::Enter)
                || !touches().is_empty())
        {
            game.reset();
        }

        game.update(dt, left, right, jump, attack, dash, slow, throw_shuriken);

        set_camera(&Camera2D {
            target: vec2(VIEW_W / 2.0, VIEW_H / 2.0),
            zoom: vec2(2.0 / screen_width(), -2.0 / screen_height()),
            offset: vec2(0.0, 0.0),
            ..Default::default()
        });
        clear_background(Color::from_rgba(5, 7, 18, 255));

        draw_texture_ex(
            &assets.city,
            -game.camera,
            0.0,
            WHITE,
            DrawTextureParams {
                dest_size: Some(vec2(WORLD_W, 240.0)),
                source: Some(Rect::new(0.0, 0.0, 1200.0, 240.0)),
                ..Default::default()
            },
        );
        draw_texture_ex(
            &assets.city,
            -game.camera,
            240.0,
            WHITE,
            DrawTextureParams {
                dest_size: Some(vec2(WORLD_W, 30.0)),
                source: Some(Rect::new(0.0, 210.0, 1200.0, 30.0)),
                ..Default::default()
            },
        );

        for enemy in &game.enemies {
            draw_enemy(enemy, &game, &assets);
        }
        for p in &game.projectiles {
            draw_texture_ex(
                &assets.shuriken,
                p.x - game.camera - 10.0,
                p.y - 10.0,
                WHITE,
                DrawTextureParams {
                    dest_size: Some(vec2(20.0, 20.0)),
                    source: Some(Rect::new(0.0, 0.0, 8.0, 8.0)),
                    rotation: game.elapsed * 13.0,
                    pivot: Some(vec2(10.0, 10.0)),
                    ..Default::default()
                },
            );
        }
        draw_player(&game, &assets);

        draw_text("NEON BLADE // SECTOR 07", 10.0, 14.0, 10.0, Color::from_rgba(78, 225, 245, 255));
        draw_text(&format!("HP {}", "◆".repeat(game.hp.max(0) as usize)), 10.0, 28.0, 10.0, PINK);
        draw_text(&format!("ELIMINATED {}/4", game.kills), 365.0, 14.0, 10.0, WHITE);
        if game.enemies.get(3).map(|e| e.alive).unwrap_or(false) {
            draw_text("DEMON SAMURAI", 336.0, 29.0, 8.0, Color::from_rgba(255, 85, 112, 255));
        }

        if game.won || game.dead {
            draw_rectangle(0.0, 0.0, VIEW_W, VIEW_H, Color::from_rgba(3, 7, 20, 220));
            let msg = if game.won { "MISSION COMPLETE" } else { "SYSTEM FAILURE" };
            let d = measure_text(msg, None, 25, 1.0);
            draw_text(msg, VIEW_W / 2.0 - d.width / 2.0, 124.0, 25.0, if game.won { SKYBLUE } else { PINK });
            draw_text("TAP / ENTER TO RESTART", 165.0, 150.0, 10.0, WHITE);
        } else {
            button(22.0, 224.0, 62.0, 38.0, "<");
            button(91.0, 224.0, 62.0, 38.0, ">");
            button(310.0, 224.0, 78.0, 38.0, "JUMP");
            button(390.0, 224.0, 72.0, 38.0, "SLASH");
            button(310.0, 177.0, 78.0, 38.0, "DASH");
            button(390.0, 177.0, 72.0, 38.0, "SLOW");
            button(390.0, 132.0, 72.0, 38.0, "SHURIKEN");
        }
        next_frame().await;
    }
}
