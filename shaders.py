'''
 * Nombre: shaders.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode, pygame, OpenGL
 * Historial: Finalizado el 26.10.2023
              Modificado el 04.11.2023
 '''

# Graphics Library Shader Language: GLSL

vertex_shader = """
    #version 450 core
    layout (location = 0) in vec3 position;
    layout (location = 1) in vec2 texCoords;
    layout (location = 2) in vec3 normals;
    
    uniform mat4 modelMatrix;
    uniform mat4 viewMatrix;
    uniform mat4 projectionMatrix;
    
    out vec2 UVs;
    out vec3 normal;
    
    void main() {
        gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
        UVs = texCoords;
        normal = (modelMatrix * vec4(normals, 0.0)).xyz;
    }
"""

fragment_shader = """
    #version 450 core
    
    layout (binding = 0) uniform sampler2D tex;
    
    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;
    
    void main() {
        fragColor = texture(tex, UVs);
    }
"""

gourad_fragment_shader = """
    #version 450 core
    
    layout (binding = 0) uniform sampler2D tex;

    uniform vec3 dirLight;

    uniform float lightIntensity;

    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;
    
    void main() {
        float intensity = dot(normal, -dirLight) * lightIntensity;
        fragColor = texture(tex, UVs) * intensity;
    }
"""

cell_fragment_shader = """
    #version 450 core

    layout (binding = 0) uniform sampler2D tex;

    uniform vec3 dirLight;
    uniform float lightIntensity;
    uniform float time;

    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;

    float rand(vec2 co) {
        return fract(sin(dot(co.xy ,vec2(12.9898,78.233))) * 43758.5453);
    }

    void main() {
        float edgeSens = 0.4 + 0.1 * sin(time + rand(UVs));
        float intensity = 0.85 + 0.15 * sin(time + rand(UVs));

        float gouraudIntensity = dot(normal, -dirLight) * lightIntensity;
        vec4 color = texture(tex, UVs) * gouraudIntensity;
        
        float gintensity = 0.2989 * color.r + 0.5870 * color.g + 0.1140 * color.b;
        
        if (gintensity > edgeSens) {
            fragColor = color;
        } else if (gintensity > intensity) {
            fragColor = vec4(0, 0, 0, 1);
        } else {
            fragColor = vec4(0, 0, 0, 1);
        }
    }

"""

multicolor_fragment_shader = """
    #version 450 core

    layout (binding = 0) uniform sampler2D tex;

    uniform vec3 dirLight;
    uniform float lightIntensity;
    uniform float time;

    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;

    void main() {
        float intensity = dot(normal, -dirLight) * lightIntensity;
        vec3 gradientColor = vec3(UVs.y + sin(time * normal.x), UVs.x + cos(time * normal.y), 1.0 - UVs.x + tan(time * normal.z));
        fragColor = vec4(gradientColor, 1.0) * intensity;
    }
"""

noise_fragment_shader = """
    #version 450 core

    layout (binding = 0) uniform sampler2D tex;
    layout (binding = 1) uniform sampler2D noiseTex;

    uniform vec3 dirLight;
    uniform float lightIntensity;
    uniform float time;

    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;

    void main() {
        float edgeSens = 0.4;
        float intensity = 0.85;

        float gouraudIntensity = dot(normal, -dirLight) * lightIntensity;

        vec2 noiseCoords = UVs + vec2(time * -0.1);
        float noise = texture(noiseTex, noiseCoords).r;
        vec2 distortedCoords = UVs + vec2(noise * 0.1 + sin(time) * 0.05);
        vec4 color = texture(tex, UVs) * gouraudIntensity;

        float gintensity = 0.2989 * color.r + 0.5870 * color.g + 0.1140 * color.b;
        
        if (noise > 0.8) {
            if (gintensity > edgeSens) {
                fragColor = color;
            } else if (gintensity > intensity) {
                fragColor = vec4(0, 0, 0, 1);
            } else {
                fragColor = vec4(0, 0, 0, 1);
            }
        } else {
            fragColor = texture(noiseTex, distortedCoords);
        }
    }

"""

party_fragment_shader = """
    #version 450 core

    layout (binding = 0) uniform sampler2D tex;

    uniform vec3 dirLight;
    uniform float lightIntensity;
    uniform float time;

    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;

    void main() {
        float intensity = dot(normal, -dirLight) * lightIntensity;

        // Definir los colores tricolor
        vec3 pink = vec3(1.0, 0.0, 0.5);
        vec3 purple = vec3(0.5, 0.0, 0.5);
        vec3 cyan = vec3(0.0, 0.5, 0.7);

        // Calcular el color tricolor basado en el tiempo
        vec3 tricolorColor = mix(pink, mix(purple, cyan, fract(time)), fract(time + 0.3333));

        fragColor = vec4(tricolorColor, 1.0) * intensity;
    }
"""

sparkling_fragment_shader = """
    #version 450 core

    layout (binding = 0) uniform sampler2D tex;

    uniform vec3 dirLight;
    uniform float lightIntensity;
    uniform float time;

    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;

    void main() {
        float intensity = dot(normal, -dirLight) * lightIntensity;

        // Muestrear la textura original en función de las coordenadas UV
        vec4 originalColor = texture(tex, UVs);

        // Agregar un movimiento cíclico a los colores usando el tiempo
        float cycleSpeed = 2.0; // Ajusta la velocidad del ciclo
        originalColor = originalColor * (1.0 + 0.5 * sin(time * cycleSpeed));

        fragColor = originalColor * vec4(vec3(1.0), 1.0) * intensity;
    }
"""

distorsioned_fragment_shader = """
    #version 450 core

    layout (binding = 0) uniform sampler2D tex;

    uniform vec3 dirLight;
    uniform float lightIntensity;
    uniform float time;

    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;

    void main() {
        float intensity = dot(normal, -dirLight) * lightIntensity;

        // Agregar un efecto de ondulación (movimiento tipo agua) a los colores
        float waveFrequency = 5.0; // Ajusta la frecuencia de las ondas
        float waveAmplitude = 0.1; // Ajusta la amplitud de las ondas
        vec2 distortedUV = UVs + vec2(waveAmplitude * sin(UVs.y * waveFrequency + time), 0.0);

        fragColor = texture(tex, distortedUV) * intensity;
    }
"""
