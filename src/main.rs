use macroquad::prelude::*;

const WORLD_W: f32 = 2240.0;
const FLOOR_Y: f32 = 207.0;
const VIEW_W: f32 = 480.0;
const VIEW_H: f32 = 270.0;

#[derive(Clone, Copy)]
struct Actor { x:f32, y:f32, vx:f32, vy:f32, alive:bool }
impl Actor { fn new(x:f32,y:f32)->Self { Self{x,y,vx:0.0,vy:0.0,alive:true} } }

struct Game {
    player: Actor, enemies: Vec<Actor>, camera:f32, hp:i32, kills:i32,
    elapsed:f32, slash:f32, won:bool, dead:bool, invuln:f32,
}
impl Game {
    fn new()->Self {
        Self { player:Actor::new(80.0,178.0),
            enemies:vec![Actor::new(520.0,178.0),Actor::new(930.0,178.0),Actor::new(1480.0,178.0)],
            camera:0.0,hp:3,kills:0,elapsed:0.0,slash:0.0,won:false,dead:false,invuln:0.0 }
    }
    fn reset(&mut self) { *self=Self::new(); }
    fn update(&mut self,dt:f32,left:bool,right:bool,jump:bool,attack:bool,slow:bool) {
        if self.won || self.dead { return; }
        self.elapsed+=dt; self.slash=(self.slash-dt).max(0.0); self.invuln=(self.invuln-dt).max(0.0);
        let step=if slow {dt*0.42} else {dt};
        let dir=(right as i32-left as i32) as f32;
        self.player.vx=dir*145.0;
        if jump && self.player.y>=FLOOR_Y-30.5 { self.player.vy=-300.0; }
        self.player.vy=(self.player.vy+760.0*step).min(430.0);
        let old_y=self.player.y;
        self.player.x=(self.player.x+self.player.vx*step).clamp(0.0,WORLD_W-22.0);
        self.player.y+=self.player.vy*step;
        let platforms=[(0.0,410.0,FLOOR_Y),(470.0,760.0,FLOOR_Y),(825.0,1210.0,FLOOR_Y),(1280.0,1630.0,FLOOR_Y),(1710.0,WORLD_W,FLOOR_Y),(300.0,380.0,164.0),(690.0,755.0,150.0),(1090.0,1160.0,165.0),(1510.0,1590.0,145.0)];
        for (l,r,top) in platforms {
            if self.player.x+22.0>l && self.player.x<r && old_y+29.0<=top+5.0 && self.player.y+29.0>=top && self.player.vy>=0.0 {
                self.player.y=top-29.0; self.player.vy=0.0;
            }
        }
        if self.player.y>310.0 { self.damage(); self.player.x=(self.player.x-100.0).max(30.0); self.player.y=150.0; self.player.vy=0.0; }
        if attack && self.slash<=0.0 {
            self.slash=0.28;
            for e in &mut self.enemies {
                if e.alive && (e.x-self.player.x).abs()<76.0 && (e.y-self.player.y).abs()<55.0 { e.alive=false; self.kills+=1; }
            }
        }
        for i in 0..self.enemies.len() {
            if !self.enemies[i].alive { continue; }
            let dx=self.player.x-self.enemies[i].x;
            if dx.abs()<185.0 {
                self.enemies[i].vx=if dx>0.0 {42.0} else {-42.0};
                self.enemies[i].x+=self.enemies[i].vx*step;
                if dx.abs()<23.0 && self.invuln<=0.0 { self.damage(); self.invuln=0.9; }
            }
        }
        self.camera=(self.player.x-160.0).clamp(0.0,WORLD_W-VIEW_W);
        if self.player.x>2110.0 { self.won=true; }
    }
    fn damage(&mut self) { self.hp-=1; if self.hp<=0 {self.dead=true;} }
}

fn draw_actor(tex:&Texture2D,x:f32,y:f32,camera:f32,enemy:bool) {
    let src=Rect::new(if enemy {32.0}else{0.0},0.0,32.0,32.0);
    draw_texture_ex(tex,x-camera,y,WHITE,DrawTextureParams{dest_size:Some(vec2(28.0,31.0)),source:Some(src),..Default::default()});
    if enemy { draw_rectangle(x-camera+8.0,y+2.0,18.0,2.0,Color::from_rgba(255,56,146,255)); }
}
fn button(x:f32,y:f32,w:f32,h:f32,label:&str) {
    draw_rectangle(x,y,w,h,Color::from_rgba(8,22,43,190));
    draw_rectangle_lines(x,y,w,h,1.0,Color::from_rgba(31,181,206,255));
    let fs=if label.len()>3 {8.0}else{17.0};
    let d=measure_text(label,None,fs as u16,1.0);
    draw_text(label,x+(w-d.width)/2.0,y+h/2.0+fs*0.35,fs,WHITE);
}
fn touch_state()->(bool,bool,bool,bool,bool) {
    let mut left=false; let mut right=false; let mut jump=false; let mut attack=false; let mut slow=false;
    let (sw,sh)=(screen_width(),screen_height());
    for t in touches() {
        let x=t.position.x*VIEW_W/sw; let y=t.position.y*VIEW_H/sh;
        if x<88.0 && y>205.0 {left=true}
        if (89.0..160.0).contains(&x) && y>205.0 {right=true}
        if (315.0..390.0).contains(&x) && y>205.0 {jump=true}
        if x>390.0 && y>205.0 {attack=true}
        if x>390.0 && (165.0..215.0).contains(&y) {slow=true}
    }
    (left,right,jump,attack,slow)
}
#[macroquad::main("NEON BLADE")]
async fn main() {
    set_pc_assets_folder("assets");
    let bg=load_texture("city.png").await.ok();
    let sprites=load_texture("sprites.png").await.ok();
    let tile=load_texture("metal_tile.png").await.ok();
    if let Some(t)=&sprites {t.set_filter(FilterMode::Nearest);}
    if let Some(t)=&tile {t.set_filter(FilterMode::Nearest);}
    if let Some(t)=&bg {t.set_filter(FilterMode::Nearest);}
    let mut game=Game::new();
    loop {
        let dt=get_frame_time().min(0.033);
        let (mut left,mut right,mut jump,mut attack,mut slow)=touch_state();
        left|=is_key_down(KeyCode::Left)||is_key_down(KeyCode::A);
        right|=is_key_down(KeyCode::Right)||is_key_down(KeyCode::D);
        jump|=is_key_pressed(KeyCode::Space)||is_key_down(KeyCode::Up);
        attack|=is_key_down(KeyCode::Z)||is_mouse_button_down(MouseButton::Left);
        slow|=is_key_down(KeyCode::X);
        if (game.won||game.dead) && (is_mouse_button_pressed(MouseButton::Left)||is_key_pressed(KeyCode::Enter)||!touches().is_empty()) {game.reset();}
        game.update(dt,left,right,jump,attack,slow);

        let scale=(screen_width()/VIEW_W).min(screen_height()/VIEW_H);
        let ox=(screen_width()-VIEW_W*scale)/2.0; let oy=(screen_height()-VIEW_H*scale)/2.0;
        set_camera(&Camera2D{target:vec2(VIEW_W/2.0,VIEW_H/2.0),zoom:vec2(2.0/screen_width(),-2.0/screen_height()),offset:vec2(0.0,0.0),..Default::default()});
        clear_background(Color::from_rgba(4,7,19,255));
        // Render in a fixed 480x270 virtual canvas.
        let _=ox; let _=oy; let _=scale;
        if let Some(t)=&bg {
            let par=(game.camera*0.28)%480.0;
            draw_texture_ex(t,-par,0.0,WHITE,DrawTextureParams{dest_size:Some(vec2(480.0,270.0)),..Default::default()});
            draw_texture_ex(t,480.0-par,0.0,WHITE,DrawTextureParams{dest_size:Some(vec2(480.0,270.0)),..Default::default()});
        }
        for i in 0..90 {
            let x=((i as f32*71.0-game.camera*0.72)%480.0+480.0)%480.0;
            let y=(i as f32*43.0+game.elapsed*(65.0+(i%30) as f32))%270.0;
            draw_line(x,y,x-3.0,y+8.0,1.0,Color::from_rgba(30,90,140,190));
        }
        let platforms=[(0.0,410.0,207.0,270.0),(470.0,760.0,207.0,270.0),(825.0,1210.0,207.0,270.0),(1280.0,1630.0,207.0,270.0),(1710.0,2240.0,207.0,270.0),(300.0,380.0,164.0,174.0),(690.0,755.0,150.0,160.0),(1090.0,1160.0,165.0,175.0),(1510.0,1590.0,145.0,155.0)];
        for (l,r,top,bottom) in platforms {
            let x=l-game.camera; let w=r-l;
            if x+w<0.0||x>480.0 {continue}
            if let Some(t)=&tile {
                let mut xx=x;
                while xx<x+w { let ww=(16.0-(xx-x)%16.0).min(x+w-xx); draw_texture_ex(t,xx,top,WHITE,DrawTextureParams{dest_size:Some(vec2(ww,bottom-top)),..Default::default()}); xx+=ww.max(1.0); }
            } else {draw_rectangle(x,top,w,bottom-top,Color::from_rgba(35,55,75,255));}
            draw_rectangle(x,top,w,2.0,Color::from_rgba(29,181,206,255));
        }
        if let Some(s)=&sprites {
            for e in &game.enemies {if e.alive {draw_actor(s,e.x,e.y,game.camera,true);}}
            draw_actor(s,game.player.x,game.player.y,game.camera,false);
        } else {
            draw_rectangle(game.player.x-game.camera,game.player.y,22.0,29.0,SKYBLUE);
            for e in &game.enemies {if e.alive {draw_rectangle(e.x-game.camera,e.y,22.0,29.0,PINK);}}
        }
        if game.slash>0.0 {draw_circle_lines(game.player.x-game.camera+15.0,game.player.y+15.0,36.0,3.0,Color::from_rgba(93,232,255,230));}
        draw_text("NEON BLADE  //  SECTOR 07",10.0,14.0,10.0,Color::from_rgba(78,225,245,255));
        draw_text(&format!("HP {}", "◆".repeat(game.hp.max(0) as usize)),10.0,28.0,10.0,PINK);
        draw_text(&format!("ELIMINATED {}/3",game.kills),370.0,14.0,10.0,WHITE);
        if game.won||game.dead {
            draw_rectangle(0.0,0.0,480.0,270.0,Color::from_rgba(3,7,20,220));
            let msg=if game.won {"MISSION COMPLETE"}else{"SYSTEM FAILURE"};
            let d=measure_text(msg,None,25,1.0);
            draw_text(msg,240.0-d.width/2.0,124.0,25.0,if game.won {SKYBLUE}else{PINK});
            draw_text("TAP / ENTER TO RESTART",165.0,150.0,10.0,WHITE);
        } else {
            button(22.0,224.0,62.0,38.0,"<"); button(91.0,224.0,62.0,38.0,">");
            button(324.0,224.0,62.0,38.0,"JUMP"); button(395.0,224.0,62.0,38.0,"SLASH"); button(395.0,177.0,62.0,35.0,"SLOW");
        }
        next_frame().await;
    }
}
