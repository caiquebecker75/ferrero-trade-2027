# Ilustrações 3D proprietárias da 75 LAB para o deck Ferrero Trade 2027 (Blender, sem interface).
#   Blender -b -P fonte/blender/cena.py -- <modo> <saída> [amostras]
# Modos: chao, ponta, balcao, ilha, familia (PNG transparente, Cycles) e montagem (MP4, EEVEE).
# Tudo é geometria nossa: tabletes genéricos nos quatro sabores, sem logotipo nem gramatura.
import bpy, math, sys, random
from mathutils import Vector

ARGS = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else ['chao', '/tmp/x.png']
MODO, SAIDA = ARGS[0], ARGS[1]
AMOSTRAS = int(ARGS[2]) if len(ARGS) > 2 else 128
FONTE = '/System/Library/Fonts/Supplemental/Georgia Bold.ttf'
random.seed(7)

bpy.ops.wm.read_factory_settings(use_empty=True)
cena = bpy.context.scene


def lin(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4) for x in c] + [1]


M = {}


def mat(nome, cor, rough=.45, metal=0., coat=0., emit=0., transm=0.):
    if nome in M:
        return M[nome]
    m = bpy.data.materials.new(nome)
    try:
        m.use_nodes = True
    except Exception:
        pass
    b = m.node_tree.nodes.get('Principled BSDF')
    b.inputs['Base Color'].default_value = lin(cor)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    if coat:
        b.inputs['Coat Weight'].default_value = coat
    if emit:
        b.inputs['Emission Color'].default_value = lin(cor)
        b.inputs['Emission Strength'].default_value = emit
    if transm:
        b.inputs['Transmission Weight'].default_value = transm
    M[nome] = m
    return m


CHOC = lambda: mat('choc', '#1A0E08', rough=.42, coat=.15)
CHOC2 = lambda: mat('choc2', '#26150C', rough=.55)
CREME = lambda: mat('creme', '#F1E6D1', rough=.5)
OURO = lambda: mat('ouro', '#C9973F', rough=.22, metal=1.)
OURO2 = lambda: mat('ouro2', '#E3BC6A', rough=.3, metal=1.)
ACRIL = lambda: mat('acril', '#FFFFFF', rough=.04, transm=1.)
LED = lambda: mat('led', '#FFE3B5', emit=8.)
SABORES = {'nozpeca': '#8A4F22', 'aoleite': '#4E2A14', 'branco': '#EDE3CC', 'dark': '#160C07'}


def caixa(nome, dims, loc, material, bevel=.004):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.name = nome
    o.scale = dims
    bpy.ops.object.transform_apply(scale=True)
    if bevel:
        md = o.modifiers.new('bv', 'BEVEL')
        md.width = bevel
        md.segments = 2
    o.data.materials.append(material)
    return o


def texto(txt, loc, tam, material, alinha='CENTER'):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0))
    o = bpy.context.object
    o.data.body = txt
    try:
        o.data.font = bpy.data.fonts.load(FONTE, check_existing=True)
    except Exception:
        pass
    o.data.size = tam
    o.data.extrude = .0015
    o.data.align_x = alinha
    o.data.align_y = 'CENTER'
    o.data.materials.append(material)
    return o


def qr(nome, lado, loc):
    """Placa de identificação do ativo com um padrão de QR desenhado por nós."""
    n = 29
    img = bpy.data.images.new('qr_' + nome, n + 4, n + 4)
    px = []
    rnd = random.Random(nome)
    for y in range(n + 4):
        for x in range(n + 4):
            gx, gy = x - 2, y - 2
            dentro = 0 <= gx < n and 0 <= gy < n
            v = 1.0
            if dentro:
                finder = False
                for fx, fy in ((0, 0), (n - 7, 0), (0, n - 7)):
                    if fx <= gx < fx + 7 and fy <= gy < fy + 7:
                        finder = True
                        dx, dy = gx - fx, gy - fy
                        borda = dx in (0, 6) or dy in (0, 6)
                        miolo = 2 <= dx <= 4 and 2 <= dy <= 4
                        v = 0.0 if (borda or miolo) else 1.0
                if not finder:
                    v = 0.0 if rnd.random() < .5 else 1.0
            px += [v, v, v, 1]
    img.pixels = px
    m = bpy.data.materials.new('qrm_' + nome)
    try:
        m.use_nodes = True
    except Exception:
        pass
    nt = m.node_tree
    tx = nt.nodes.new('ShaderNodeTexImage')
    tx.image = img
    tx.interpolation = 'Closest'
    nt.links.new(tx.outputs['Color'], nt.nodes['Principled BSDF'].inputs['Base Color'])
    nt.nodes['Principled BSDF'].inputs['Roughness'].default_value = .5
    bpy.ops.mesh.primitive_plane_add(size=lado, location=loc, rotation=(math.radians(90), 0, 0))
    o = bpy.context.object
    o.name = nome
    o.data.materials.append(m)
    return o


def junta(objs, nome):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        for md in list(o.modifiers):
            bpy.context.view_layer.objects.active = o
            bpy.ops.object.modifier_apply(modifier=md.name)
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    o = bpy.context.object
    o.name = nome
    return o


MODELOS = {}


def modelo_tablete(sabor):
    """Tablete em pé, origem na base, frente para -Y: corpo, faixa dourada e selo."""
    if sabor in MODELOS:
        return MODELOS[sabor]
    corpo = caixa('c', (.08, .012, .16), (0, 0, .08), mat('emb_' + sabor, SABORES[sabor], rough=.32, coat=.3), bevel=.0025)
    faixa = caixa('f', (.0806, .0126, .02), (0, 0, .112), OURO(), bevel=0)
    fio = caixa('f2', (.0806, .0126, .004), (0, 0, .03), OURO(), bevel=0)
    bpy.ops.mesh.primitive_cylinder_add(radius=.016, depth=.002, location=(0, -.0068, .112), rotation=(math.radians(90), 0, 0), vertices=40)
    selo = bpy.context.object
    selo.data.materials.append(OURO2())
    o = junta([corpo, faixa, fio, selo], 'tablete_' + sabor)
    o.hide_render = True
    o.location = (0, 0, -50)
    MODELOS[sabor] = o
    return o


TABLETES = []


def tablete(sabor, loc, rot=0., parte=None):
    m = modelo_tablete(sabor)
    o = m.copy()
    bpy.context.collection.objects.link(o)
    o.hide_render = False
    o.location = loc
    o.rotation_euler = (0, 0, math.radians(rot))
    TABLETES.append((o, parte))
    return o


def fileira(sabor, x0, x1, passo, y, z, fundo=3, rot=0., parte=None, eixo='x'):
    n = int(round((x1 - x0) / passo)) + 1
    for i in range(n):
        for k in range(fundo):
            d = k * .014
            if eixo == 'x':
                tablete(sabor, (x0 + i * passo, y + (d if y < 0 else -d), z), rot, parte)
            else:
                tablete(sabor, (y + (d if y < 0 else -d), x0 + i * passo, z), rot, parte)


# ---------------------------------------------------------------- peças
def display_chao(ox=0., grupos=None):
    g = grupos if grupos is not None else {}
    add = lambda k, o: g.setdefault(k, []).append(o)
    W, D = .62, .40
    add('base', caixa('base', (W, D, .12), (ox, 0, .06), CHOC(), bevel=.008))
    add('base', caixa('friso', (W - .02, .004, .014), (ox, -D / 2 - .002, .095), OURO(), bevel=0))
    for s in (-1, 1):
        add('lados', caixa('lado', (.022, D, 1.30), (ox + s * (W / 2 - .011), 0, .12 + .65), CHOC2(), bevel=.004))
        add('lados', caixa('filete', (.006, .006, 1.28), (ox + s * (W / 2 - .011), -D / 2 - .001, .12 + .65), OURO(), bevel=0))
    add('fundo', caixa('fundo', (W - .044, .02, 1.30), (ox, D / 2 - .03, .77), CHOC2(), bevel=0))
    add('fundo', caixa('painel', (W - .05, .004, 1.27), (ox, D / 2 - .042, .775), mat('painel', '#E7D5B5', rough=.6), bevel=0))
    sab = ['dark', 'branco', 'aoleite', 'nozpeca']
    for i, z in enumerate((.20, .50, .80, 1.10)):
        pr = [caixa('prat', (W - .046, .34, .016), (ox, -.01, z), CREME(), bevel=.003),
              caixa('lip', (W - .046, .006, .04), (ox, -.18, z + .02), ACRIL(), bevel=.001),
              caixa('etq', (W - .046, .004, .018), (ox, -.183, z - .002), OURO(), bevel=0)]
        g.setdefault('prat%d' % i, []).extend(pr)
        fileira(sab[i], ox - .25, ox + .25, .1, -.15, z + .008, fundo=3, parte='prat%d' % i)
    hd = [caixa('frontao_aro', (W + .05, .05, .32), (ox, D / 2 - .03, 1.585), OURO(), bevel=.004),
          caixa('frontao', (W + .03, .056, .30), (ox, D / 2 - .03, 1.585), CHOC(), bevel=.004),
          texto('O NOVO SABOR', (ox, D / 2 - .059, 1.665), .028, OURO2()),
          texto('Noz-Pecã', (ox, D / 2 - .059, 1.585), .07, CREME()),
          texto('& Avelã', (ox, D / 2 - .059, 1.515), .045, CREME())]
    g.setdefault('frontao', []).extend(hd)
    add('id', caixa('placa', (.07, .004, .07), (ox + .2, -D / 2 - .003, .06), CREME(), bevel=.002))
    add('id', qr('qr%.2f' % ox, .056, (ox + .2, -D / 2 - .0055, .06)))
    return g


def ponta(ox=0.):
    W, D = 1.0, .45
    caixa('base', (W, D, .12), (ox, 0, .06), CHOC(), bevel=.008)
    caixa('friso', (W - .02, .004, .014), (ox, -D / 2 - .002, .095), OURO(), bevel=0)
    for s in (-1, 1):
        caixa('lado', (.03, D + .02, 1.55), (ox + s * (W / 2 - .015), 0, .12 + .775), CHOC2(), bevel=.005)
        caixa('filete', (.008, .006, 1.53), (ox + s * (W / 2 - .015), -D / 2 - .011, .12 + .775), OURO(), bevel=0)
    caixa('fundo', (W - .06, .02, 1.55), (ox, D / 2 - .03, .895), CHOC2(), bevel=0)
    caixa('painel', (W - .07, .004, 1.52), (ox, D / 2 - .042, .9), mat('painel', '#E7D5B5', rough=.6), bevel=0)
    sab = ['dark', 'branco', 'aoleite', 'nozpeca', 'nozpeca']
    for i, z in enumerate((.14, .42, .70, .98, 1.26)):
        caixa('prat', (W - .06, .38, .016), (ox, -.02, z), CREME(), bevel=.003)
        caixa('lip', (W - .06, .006, .04), (ox, -.21, z + .02), ACRIL(), bevel=.001)
        caixa('etq', (W - .06, .004, .018), (ox, -.213, z - .002), OURO(), bevel=0)
        caixa('led', (W - .08, .01, .006), (ox, -.19, z - .012), LED(), bevel=0)
        fileira(sab[i], ox - .405, ox + .405, .09, -.17, z + .008, fundo=3)
    caixa('frontao_aro', (W + .07, .05, .40), (ox, D / 2 - .03, 1.88), OURO(), bevel=.004)
    caixa('frontao', (W + .05, .056, .38), (ox, D / 2 - .03, 1.88), CHOC(), bevel=.004)
    texto('LINHA DE TABLETES', (ox, D / 2 - .059, 1.99), .035, OURO2())
    texto('Quatro sabores,', (ox, D / 2 - .059, 1.895), .075, CREME())
    texto('um momento seu', (ox, D / 2 - .059, 1.80), .075, CREME())
    caixa('led_topo', (W, .01, .008), (ox, D / 2 - .06, 1.675), LED(), bevel=0)


def balcao(ox=0., oz=0.):
    W = .44
    caixa('base', (W, .30, .03), (ox, 0, oz + .015), CHOC(), bevel=.004)
    caixa('degrau1', (W - .02, .13, .06), (ox, -.075, oz + .06), CHOC2(), bevel=.003)
    caixa('degrau2', (W - .02, .13, .15), (ox, .055, oz + .105), CHOC2(), bevel=.003)
    caixa('friso1', (W - .02, .004, .01), (ox, -.142, oz + .085), OURO(), bevel=0)
    caixa('friso2', (W - .02, .004, .01), (ox, -.012, oz + .175), OURO(), bevel=0)
    caixa('costas_aro', (W + .02, .025, .36), (ox, .135, oz + .3), OURO(), bevel=.003)
    caixa('costas', (W, .03, .34), (ox, .135, oz + .3), CHOC(), bevel=.003)
    texto('NOVO', (ox, .118, oz + .43), .03, OURO2())
    texto('Noz-Pecã', (ox, .118, oz + .385), .045, CREME())
    for i, s in enumerate(['nozpeca', 'aoleite', 'branco', 'dark']):
        x = ox - .1425 + i * .095
        for k in range(2):
            tablete(s, (x, -.11 + k * .014, oz + .09))
            tablete(s, (x, .02 + k * .014, oz + .18))
    qr('qrb', .036, (ox + .17, -.1515, oz + .015 + .0))


def ilha(ox=0.):
    caixa('t1', (1.2, .8, .30), (ox, 0, .15), CHOC(), bevel=.01)
    caixa('t1f', (1.204, .804, .012), (ox, 0, .29), OURO(), bevel=0)
    caixa('t2', (.86, .52, .22), (ox, 0, .41), CHOC2(), bevel=.008)
    caixa('t2f', (.864, .524, .01), (ox, 0, .515), OURO(), bevel=0)
    caixa('t3', (.52, .28, .20), (ox, 0, .62), CHOC(), bevel=.008)
    caixa('t3f', (.524, .284, .01), (ox, 0, .715), OURO(), bevel=0)
    fileira('aoleite', ox - .55, ox + .55, .1, -.36, .30, fundo=2)
    fileira('dark', ox - .55, ox + .55, .1, .36, .30, fundo=2, rot=180)
    fileira('branco', -.2, .2, .1, ox - .55, .30, fundo=2, rot=-90, eixo='y')
    fileira('branco', -.2, .2, .1, ox + .55, .30, fundo=2, rot=90, eixo='y')
    fileira('branco', ox - .37, ox + .37, .0925, -.235, .52, fundo=2)
    fileira('aoleite', ox - .37, ox + .37, .0925, .235, .52, fundo=2, rot=180)
    fileira('nozpeca', ox - .2, ox + .2, .1, -.115, .72, fundo=2)
    fileira('nozpeca', ox - .2, ox + .2, .1, .115, .72, fundo=2, rot=180)
    caixa('totem', (.1, .1, .62), (ox, 0, 1.03), OURO(), bevel=.004)
    caixa('placa_aro', (.62, .05, .34), (ox, 0, 1.5), OURO(), bevel=.004)
    caixa('placa', (.60, .058, .32), (ox, 0, 1.5), CHOC(), bevel=.004)
    texto('LANÇAMENTO', (ox, -.03, 1.58), .03, OURO2())
    texto('Noz-Pecã', (ox, -.03, 1.505), .07, CREME())
    texto('& Avelã', (ox, -.03, 1.435), .045, CREME())


# ---------------------------------------------------------------- luz, câmera, render
def luzes(escala=1.):
    for nome, loc, pot, tam in (('key', (-2.4, -3.2, 3.4), 900, 2.4), ('fill', (3.2, -2.2, 1.6), 300, 2.), ('rim', (.5, 3.4, 3.2), 650, 2.)):
        d = bpy.data.lights.new(nome, 'AREA')
        d.energy = pot * escala * escala
        d.size = tam * escala
        d.color = (1, .95, .88) if nome != 'rim' else (1, .9, .75)
        o = bpy.data.objects.new(nome, d)
        bpy.context.collection.objects.link(o)
        o.location = Vector(loc) * escala
        dirc = Vector((0, 0, .8 * escala)) - o.location
        o.rotation_euler = dirc.to_track_quat('-Z', 'Y').to_euler()


def camera(alvo, dist, ang=-28., alt=.32, lente=50):
    d = bpy.data.cameras.new('cam')
    d.lens = lente
    c = bpy.data.objects.new('cam', d)
    bpy.context.collection.objects.link(c)
    a = math.radians(ang)
    c.location = Vector(alvo) + Vector((math.sin(a) * dist, -math.cos(a) * dist, alt * dist))
    vazio = bpy.data.objects.new('alvo', None)
    bpy.context.collection.objects.link(vazio)
    vazio.location = alvo
    k = c.constraints.new('TRACK_TO')
    k.target = vazio
    k.track_axis = 'TRACK_NEGATIVE_Z'
    k.up_axis = 'UP_Y'
    cena.camera = c
    return c, vazio


def mundo(cor, forca):
    w = bpy.data.worlds.new('mundo')
    cena.world = w
    try:
        w.use_nodes = True
    except Exception:
        pass
    bg = w.node_tree.nodes.get('Background')
    bg.inputs['Color'].default_value = lin(cor)
    bg.inputs['Strength'].default_value = forca


def chao_sombra():
    bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
    p = bpy.context.object
    p.is_shadow_catcher = True
    return p


def render_cycles(w, h):
    cena.render.engine = 'CYCLES'
    try:
        prefs = bpy.context.preferences.addons['cycles'].preferences
        prefs.compute_device_type = 'METAL'
        prefs.get_devices()
        for dv in prefs.devices:
            dv.use = True
        cena.cycles.device = 'GPU'
    except Exception as e:
        print('GPU indisponível:', e)
    cena.cycles.samples = AMOSTRAS
    cena.cycles.use_denoising = True
    cena.render.film_transparent = True
    cena.render.resolution_x, cena.render.resolution_y = w, h
    cena.render.image_settings.file_format = 'PNG'
    cena.render.image_settings.color_mode = 'RGBA'
    cena.view_settings.view_transform = 'Standard'
    cena.view_settings.exposure = -.35
    cena.render.filepath = SAIDA
    bpy.ops.render.render(write_still=True)


# ---------------------------------------------------------------- modos
if MODO in ('chao', 'ponta', 'balcao', 'ilha', 'familia'):
    mundo('#FFF4E6', .18)
    chao_sombra()
    if MODO == 'chao':
        display_chao()
        luzes()
        camera((0, 0, .86), 3.05, ang=-30, alt=.26)
        render_cycles(1100, 1500)
    elif MODO == 'ponta':
        ponta()
        luzes()
        camera((0, 0, 1.0), 4.0, ang=-30, alt=.24)
        render_cycles(1200, 1500)
    elif MODO == 'balcao':
        balcao()
        luzes(.35)
        camera((0, 0, .2), 1.55, ang=-30, alt=.38)
        render_cycles(1400, 1150)
    elif MODO == 'ilha':
        ilha()
        luzes(1.1)
        camera((0, 0, .7), 4.3, ang=-32, alt=.42)
        render_cycles(1500, 1200)
    else:
        ponta(-1.75)
        display_chao(-.5)
        ilha(.95)
        caixa('checkout', (.62, .5, .92), (2.3, 0, .46), mat('balcao_loja', '#CFC3AE', rough=.55), bevel=.01)
        caixa('tampo', (.66, .54, .03), (2.3, 0, .935), CHOC(), bevel=.004)
        balcao(2.3, .95)
        luzes(1.5)
        camera((.25, 0, .95), 7.6, ang=-14, alt=.2, lente=45)
        render_cycles(2600, 1250)

elif MODO == 'montagem':
    # Animação: o display de chão se monta peça por peça, recebe os tabletes e volta a se abrir (loop).
    mundo('#24160F', .9)
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))
    chao = bpy.context.object
    chao.data.materials.append(mat('chao', '#24160F', rough=.6))
    g = display_chao()
    luzes()
    cam, alvo = camera((0, 0, .92), 5.2, ang=-30, alt=.2)
    F = 180
    cena.frame_start, cena.frame_end = 1, F
    cena.render.fps = 30
    desloca = {'base': (0, 0, -.5), 'lados': None, 'fundo': (0, .7, 0), 'frontao': (0, 0, .7), 'id': (0, -.5, 0)}
    for i in range(4):
        desloca['prat%d' % i] = (0, -.9 - .15 * i, .1 * i)
    ordem = ['base', 'lados', 'fundo', 'prat0', 'prat1', 'prat2', 'prat3', 'frontao', 'id']

    def chave(o, f, loc=None, esc=None):
        if loc is not None:
            o.location = loc
            o.keyframe_insert('location', frame=f)
        if esc is not None:
            o.scale = (esc, esc, esc)
            o.keyframe_insert('scale', frame=f)

    for idx, k in enumerate(ordem):
        f0 = 10 + idx * 6
        for o in g.get(k, []):
            base = o.location.copy()
            if k == 'lados':
                d = Vector((.45 if base.x > 0 else -.45, 0, 0))
            else:
                d = Vector(desloca[k])
            chave(o, 1, base + d)
            chave(o, f0, base + d)
            chave(o, f0 + 22, base)
            chave(o, 150 - idx * 3, base)
            chave(o, 176, base + d)
    for j, (o, parte) in enumerate(TABLETES):
        i = int(parte[-1]) if parte else 0
        f0 = 72 + (3 - i) * 8 + (j % 18) // 3
        base = o.location.copy()
        chave(o, 1, base + Vector((0, 0, .25)), .001)
        chave(o, f0, base + Vector((0, 0, .25)), .001)
        chave(o, f0 + 10, base, 1)
        chave(o, 128, base, 1)
        chave(o, 140, base + Vector((0, 0, .25)), .001)
    # câmera em vaivém suave: começa e termina no mesmo lugar
    for f in range(1, F + 1, 3):
        a = math.radians(-30 + 16 * math.sin(2 * math.pi * (f - 1) / F))
        cam.location = Vector((0, 0, .92)) + Vector((math.sin(a) * 5.2, -math.cos(a) * 5.2, .2 * 5.2))
        cam.keyframe_insert('location', frame=f)
    for o in bpy.data.objects:
        ad = o.animation_data
        if ad and ad.action:
            try:
                for fc in ad.action.fcurves:
                    for kp in fc.keyframe_points:
                        kp.interpolation = 'BEZIER'
                        kp.easing = 'EASE_IN_OUT'
            except Exception:
                pass
    cena.render.engine = 'BLENDER_EEVEE'
    try:
        cena.eevee.taa_render_samples = 48
        cena.eevee.use_shadows = True
        cena.eevee.use_raytracing = False
    except Exception:
        pass
    cena.render.resolution_x, cena.render.resolution_y = 1280, 720
    cena.view_settings.view_transform = 'Standard'
    cena.view_settings.exposure = -.35
    im = cena.render.image_settings
    try:
        im.media_type = 'VIDEO'
    except Exception:
        pass
    im.file_format = 'FFMPEG'
    cena.render.ffmpeg.format = 'MPEG4'
    cena.render.ffmpeg.codec = 'H264'
    cena.render.ffmpeg.constant_rate_factor = 'HIGH'
    cena.render.ffmpeg.ffmpeg_preset = 'GOOD'
    cena.render.filepath = SAIDA
    if len(ARGS) > 3:
        cena.frame_set(int(ARGS[3]))
        try:
            im.media_type = 'IMAGE'
        except Exception:
            pass
        im.file_format = 'PNG'
        bpy.ops.render.render(write_still=True)
    else:
        bpy.ops.render.render(animation=True)
