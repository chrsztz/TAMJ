#!/usr/bin/env python3
"""快速测试所有 Gradio API 修复"""

import sys
sys.path.insert(0, '/Users/ztz/TAMJ/FastChat')
sys.path.insert(0, '/Users/ztz/TAMJ')

print('=' * 60)
print('测试 Gradio 5.x API 兼容性修复')
print('=' * 60)

try:
    print('\n1. 导入 gradio_web_server_multi...')
    from fastchat.serve import gradio_web_server_multi
    print('   ✓ 成功')
    
    print('\n2. 导入 gradio_block_arena_named...')
    from fastchat.serve import gradio_block_arena_named
    print('   ✓ 成功')
    
    print('\n3. 导入 gradio_block_arena_anony...')
    from fastchat.serve import gradio_block_arena_anony
    print('   ✓ 成功')
    
    print('\n4. 导入 gradio_block_arena_referee...')
    from fastchat.serve import gradio_block_arena_referee
    print('   ✓ 成功')
    
    print('\n5. 测试 build_demo 创建界面...')
    from fastchat.serve.gradio_web_server_multi import build_demo
    models = ['model-1', 'model-2']
    demo = build_demo(models, None, None)
    print('   ✓ 成功创建 Gradio 界面')
    
    print('\n' + '=' * 60)
    print('🎉 所有 Gradio API 兼容性测试通过！')
    print('=' * 60)
    print('\n可以启动 Web Server 了：')
    print('  python -m fastchat.serve.gradio_web_server_multi')
    
except Exception as e:
    print(f'\n✗ 测试失败: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)

