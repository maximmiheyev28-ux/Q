import java.util.Base64
import org.gradle.api.tasks.TaskAction

plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

val decodePixelAssets by tasks.registering {
    val sourceDir = file("src/main/assets")
    val outputDir = layout.buildDirectory.dir("generated/pixelAssets")
    inputs.dir(sourceDir)
    outputs.dir(outputDir)
    doLast {
        val out = outputDir.get().asFile
        out.mkdirs()
        listOf("city.png", "sprites.png", "metal_tile.png").forEach { name ->
            val encoded = file("src/main/assets/$name.b64").readText()
            File(out, name).writeBytes(Base64.getMimeDecoder().decode(encoded))
        }
    }
}

android {
    namespace = "com.neonblade.game"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.neonblade.game"
        minSdk = 23
        targetSdk = 28
        versionCode = 1
        versionName = "0.1.0"
    }

    sourceSets.getByName("main").assets.srcDir(decodePixelAssets.map { layout.buildDirectory.dir("generated/pixelAssets").get().asFile })

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
}

tasks.named("preBuild").configure { dependsOn(decodePixelAssets) }
