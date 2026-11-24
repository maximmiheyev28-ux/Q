package com.neonblade.game

import android.content.Context
import android.graphics.*
import android.view.MotionEvent
import android.view.SurfaceHolder
import android.view.SurfaceView
import kotlin.math.abs
import kotlin.math.max
import kotlin.math.min

class NeonGameView(context: Context) : SurfaceView(context), SurfaceHolder.Callback, Runnable {
    private var loop: Thread? = null
    @Volatile private var running = false
    private val paint = Paint().apply { isFilterBitmap = false }
    private val bg: Bitmap
    private val sheet: Bitmap
    private val tile: Bitmap
    private val worldW = 2240f
    private val player = Actor(80f, 178f, 0f, 0f, 22f, 29f)
    private val enemies = mutableListOf(Actor(520f, 178f, 0f, 0f, 22f, 29f), Actor(930f, 178f, 0f, 0f, 22f, 29f), Actor(1480f, 178f, 0f, 0f, 22f, 29f))
    private val platforms = listOf(
        RectF(0f,207f,410f,270f), RectF(470f,207f,760f,270f), RectF(825f,207f,1210f,270f),
        RectF(1280f,207f,1630f,270f), RectF(1710f,207f,2240f,270f),
        RectF(300f,164f,380f,174f), RectF(690f,150f,755f,160f), RectF(1090f,165f,1160f,175f), RectF(1510f,145f,1590f,155f)
    )
    private var camera = 0f
    private var last = System.nanoTime()
    private var moveLeft = false; private var moveRight = false; private var jump = false
    private var attack = false; private var slow = false
    private var grounded = false; private var slashTime = 0f
    private var hp = 3; private var kills = 0; private var won = false; private var dead = false
    private var elapsed = 0f
    private val rain = Array(90) { floatArrayOf((it * 71 % 480).toFloat(), (it * 43 % 270).toFloat(), (it % 4 + 3).toFloat()) }

    init {
        holder.addCallback(this)
        bg = assetsBitmap("city.png")
        sheet = assetsBitmap("sprites.png")
        tile = assetsBitmap("metal_tile.png")
        isFocusable = true
    }

    private fun assetsBitmap(name: String): Bitmap = context.assets.open(name).use { BitmapFactory.decodeStream(it) }

    override fun surfaceCreated(holder: SurfaceHolder) { running = true; loop = Thread(this, "neon-game-loop").also { it.start() } }
    override fun surfaceDestroyed(holder: SurfaceHolder) { running = false; loop?.join(500) }
    override fun surfaceChanged(holder: SurfaceHolder, format: Int, width: Int, height: Int) {}

    override fun run() {
        while (running) {
            val now = System.nanoTime()
            val dt = min(0.033f, (now - last) / 1_000_000_000f)
            last = now
            update(dt)
            val c = holder.lockCanvas()
            if (c != null) {
                try { render(c) } finally { holder.unlockCanvasAndPost(c) }
            }
            try { Thread.sleep(8) } catch (_: InterruptedException) {}
        }
    }

    private fun update(dt0: Float) {
        if (won || dead) return
        val dt = if (slow) dt0 * 0.42f else dt0
        elapsed += dt0
        val dir = (if (moveRight) 1 else 0) - (if (moveLeft) 1 else 0)
        player.vx = dir * 145f
        if (jump && grounded) { player.vy = -300f; grounded = false }
        player.vy = min(430f, player.vy + 760f * dt)
        val oldY = player.y
        player.x = (player.x + player.vx * dt).coerceIn(0f, worldW - player.w)
        player.y += player.vy * dt
        grounded = false
        platforms.forEach { p ->
            if (player.x + player.w > p.left && player.x < p.right && oldY + player.h <= p.top + 5 && player.y + player.h >= p.top && player.vy >= 0) {
                player.y = p.top - player.h; player.vy = 0f; grounded = true
            }
        }
        if (player.y > 310f) { hp--; player.x = max(30f, player.x - 100f); player.y = 150f; player.vy = 0f; if (hp <= 0) dead = true }
        slashTime = max(0f, slashTime - dt0)
        if (attack && slashTime <= 0f) {
            slashTime = 0.28f
            enemies.forEach { e ->
                if (e.alive && abs((e.x + e.w/2) - (player.x + player.w/2)) < 76f && abs(e.y-player.y) < 55f) {
                    e.alive = false; kills++
                }
            }
        }
        enemies.filter { it.alive }.forEach { e ->
            val dx = player.x - e.x
            if (abs(dx) < 185f) {
                e.vx = if (dx > 0) 42f else -42f
                e.x += e.vx * dt
                if (abs(dx) < 23f && elapsed % 1.0f < dt) { hp--; if (hp <= 0) dead = true }
            }
        }
        camera = (player.x - 160f).coerceIn(0f, worldW - 480f)
        if (player.x > 2110f) won = true
    }

    private fun render(real: Canvas) {
        val sx = real.width / 480f; val sy = real.height / 270f
        real.save(); real.scale(sx, sy)
        real.drawColor(Color.rgb(4,7,19))
        val parallax = (camera * 0.28f) % 480f
        real.drawBitmap(bg, null, RectF(-parallax,0f,480f-parallax,270f), paint)
        real.drawBitmap(bg, null, RectF(480f-parallax,0f,960f-parallax,270f), paint)
        // Atmospheric rain in foreground
        rain.forEachIndexed { i, r ->
            val x = (r[0] - (camera * 0.72f) % 480f + 480f) % 480f
            val y = (r[1] + elapsed * (65f + i % 30) ) % 270f
            paint.color = if (i % 3 == 0) Color.rgb(29,105,147) else Color.rgb(30,54,105)
            real.drawLine(x,y,x-3,y+8,paint)
        }
        paint.color = Color.WHITE
        platforms.forEach { p ->
            val rect = RectF(p.left-camera,p.top,p.right-camera,p.bottom)
            if (rect.right > 0 && rect.left < 480) {
                var x = rect.left
                while (x < rect.right) {
                    val w = min(16f, rect.right-x)
                    real.drawBitmap(tile, null, RectF(x,p.top,x+w,p.bottom), paint)
                    x += 16f
                }
                paint.color = Color.rgb(29,181,206); real.drawRect(rect.left,p.top,rect.right,p.top+2,paint)
                paint.color = Color.WHITE
            }
        }
        enemies.filter { it.alive }.forEach { drawActor(real,it,true) }
        drawActor(real,player,false)
        if (slashTime > 0f) {
            paint.color = Color.argb(230,93,232,255)
            real.drawArc(RectF(player.x-camera-7,player.y-13,player.x-camera+42,player.y+34),205f,125f,false,paint.apply { style=Paint.Style.STROKE; strokeWidth=3f })
            paint.style = Paint.Style.FILL
        }
        drawHud(real)
        real.restore()
    }

    private fun drawActor(c: Canvas, a: Actor, enemy: Boolean) {
        val sx = if (enemy) 32 else 0
        val src = Rect(sx,0,sx+32,32)
        val dst = RectF(a.x-camera,a.y,a.x-camera+28,a.y+31)
        paint.color = Color.WHITE
        c.drawBitmap(sheet,src,dst,paint)
        if (enemy) {
            paint.color = Color.rgb(255,56,146)
            c.drawRect(dst.left+8,dst.top+2,dst.right-4,dst.top+4,paint)
        }
    }

    private fun drawHud(c: Canvas) {
        paint.typeface = Typeface.create("monospace",Typeface.BOLD); paint.textSize=10f
        paint.color = Color.rgb(78,225,245); c.drawText("NEON BLADE  //  SECTOR 07",10f,14f,paint)
        paint.color = Color.rgb(255,73,165); c.drawText("HP " + "◆".repeat(hp.coerceAtLeast(0)),10f,28f,paint)
        paint.color = Color.WHITE; c.drawText("ELIMINATED $kills/3",370f,14f,paint)
        if (won || dead) {
            paint.color = Color.argb(210,3,7,20); c.drawRect(0f,0f,480f,270f,paint)
            paint.textAlign = Paint.Align.CENTER; paint.textSize=25f
            paint.color = if (won) Color.rgb(71,235,245) else Color.rgb(255,63,130)
            c.drawText(if (won) "MISSION COMPLETE" else "SYSTEM FAILURE",240f,124f,paint)
            paint.textSize=11f; paint.color=Color.WHITE; c.drawText("TAP TO RESTART",240f,148f,paint); paint.textAlign=Paint.Align.LEFT
        } else {
            drawButton(c,22f,224f,62f,38f,"◀"); drawButton(c,91f,224f,62f,38f,"▶")
            drawButton(c,324f,224f,62f,38f,"JUMP"); drawButton(c,395f,224f,62f,38f,"SLASH")
            drawButton(c,395f,177f,62f,35f,"SLOW")
        }
    }

    private fun drawButton(c: Canvas,x:Float,y:Float,w:Float,h:Float,label:String) {
        paint.color=Color.argb(150,8,22,43); c.drawRect(x,y,x+w,y+h,paint)
        paint.color=Color.rgb(31,135,164); paint.style=Paint.Style.STROKE; paint.strokeWidth=1f
        c.drawRect(x,y,x+w,y+h,paint); paint.style=Paint.Style.FILL
        paint.color=Color.WHITE; paint.textSize=if(label.length>3) 8f else 17f; paint.typeface=Typeface.create("monospace",Typeface.BOLD)
        paint.textAlign=Paint.Align.CENTER; c.drawText(label,x+w/2,y+h/2+4,paint); paint.textAlign=Paint.Align.LEFT
    }

    override fun onTouchEvent(event: MotionEvent): Boolean {
        val x = event.x * 480f / width; val y = event.y * 270f / height
        if (event.action == MotionEvent.ACTION_DOWN && (won || dead)) { reset(); return true }
        if (event.action == MotionEvent.ACTION_UP || event.action == MotionEvent.ACTION_CANCEL) {
            moveLeft=false; moveRight=false; jump=false; attack=false; slow=false; return true
        }
        if (event.action == MotionEvent.ACTION_DOWN || event.action == MotionEvent.ACTION_MOVE) {
            moveLeft = x in 0f..88f && y > 205f
            moveRight = x in 89f..160f && y > 205f
            jump = x in 315f..390f && y > 205f
            attack = x > 390f && y > 205f
            slow = x > 390f && y in 165f..215f
        }
        return true
    }

    private fun reset() {
        player.x=80f; player.y=178f; player.vx=0f; player.vy=0f
        enemies.forEachIndexed { i,e -> e.x=listOf(520f,930f,1480f)[i]; e.y=178f; e.alive=true }
        hp=3; kills=0; won=false; dead=false; elapsed=0f; camera=0f
    }

    private data class Actor(var x:Float,var y:Float,var vx:Float,var vy:Float,val w:Float,val h:Float,var alive:Boolean=true)
}
