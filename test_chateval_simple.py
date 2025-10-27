#!/usr/bin/env python3
"""
ChatEval 简化测试脚本
测试多智能体 debate 功能是否正常工作
"""

import sys
import os

# 设置路径
sys.path.insert(0, '/Users/ztz/TAMJ/FastChat')
sys.path.insert(0, '/Users/ztz/TAMJ')

def test_imports():
    """测试所有必要的模块是否可以导入"""
    print("=" * 60)
    print("测试 1: 导入必要的模块")
    print("=" * 60)
    
    try:
        from fastchat.serve import gradio_web_server
        print("✓ gradio_web_server 导入成功")
        
        from fastchat.serve import gradio_block_arena_named
        print("✓ gradio_block_arena_named 导入成功")
        
        from fastchat.serve import gradio_block_arena_referee
        print("✓ gradio_block_arena_referee 导入成功")
        
        from agentverse.agentverse import AgentVerse
        print("✓ AgentVerse 导入成功")
        
        import gradio as gr
        print(f"✓ Gradio {gr.__version__} 导入成功")
        
        return True
    except Exception as e:
        print(f"✗ 导入失败: {e}")
        return False

def test_agentverse_initialization():
    """测试 AgentVerse 是否可以初始化"""
    print("\n" + "=" * 60)
    print("测试 2: AgentVerse 初始化")
    print("=" * 60)
    
    try:
        from agentverse.agentverse import AgentVerse
        
        # 尝试加载 llm_eval 任务配置
        # from_task 返回 (agentverse, agents, environments)
        backend, agents, environments = AgentVerse.from_task("agentverse/tasks/llm_eval/config.yaml")
        print(f"✓ AgentVerse 初始化成功")
        print(f"  - 代理数量: {len(backend.agents)}")
        
        for i, agent in enumerate(backend.agents):
            print(f"  - Agent {i+1}: {agent.name}")
            print(f"    角色: {agent.role_description[:50]}..." if hasattr(agent, 'role_description') and agent.role_description else "    (无角色描述)")
        
        return True
    except Exception as e:
        print(f"✗ AgentVerse 初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_referee_ui():
    """测试 Referee UI 是否可以创建"""
    print("\n" + "=" * 60)
    print("测试 3: Referee UI 创建")
    print("=" * 60)
    
    try:
        from fastchat.serve.gradio_block_arena_referee import UI
        
        ui = UI()
        print(f"✓ Referee UI 创建成功")
        print(f"  - Backend 类型: {type(ui.backend).__name__}")
        print(f"  - 代理数量: {len(ui.backend.agents)}")
        
        return True
    except Exception as e:
        print(f"✗ Referee UI 创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gradio_compatibility():
    """测试 Gradio 5.x API 兼容性"""
    print("\n" + "=" * 60)
    print("测试 4: Gradio 5.x API 兼容性")
    print("=" * 60)
    
    try:
        import gradio as gr
        
        # 测试新的 API
        update_result = gr.update(interactive=True)
        print("✓ gr.update() 工作正常")
        
        skip_result = gr.skip()
        print("✓ gr.skip() 工作正常")
        
        # 确认旧 API 不再可用
        try:
            gr.Button.update()
            print("⚠️  警告: gr.Button.update() 仍然可用 (应该已被移除)")
        except AttributeError:
            print("✓ gr.Button.update() 已正确移除 (符合 Gradio 5.x)")
        
        return True
    except Exception as e:
        print(f"✗ Gradio API 测试失败: {e}")
        return False

def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("ChatEval 功能测试")
    print("=" * 60)
    print()
    
    # 检查环境变量
    if not os.environ.get("OPENAI_API_KEY"):
        print("⚠️  警告: OPENAI_API_KEY 未设置")
        print("   多智能体 debate 功能需要 OpenAI API")
        print()
    
    results = []
    
    # 运行测试
    results.append(("模块导入", test_imports()))
    results.append(("AgentVerse 初始化", test_agentverse_initialization()))
    results.append(("Referee UI", test_referee_ui()))
    results.append(("Gradio 兼容性", test_gradio_compatibility()))
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    for name, passed in results:
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"{name}: {status}")
    
    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)
    
    print()
    print(f"总计: {total_passed}/{total_tests} 测试通过")
    
    if total_passed == total_tests:
        print()
        print("🎉 所有测试通过！ChatEval 已准备就绪。")
        print()
        print("下一步:")
        print("1. 启动 Controller: python -m fastchat.serve.controller")
        print("2. 启动 Model Workers")
        print("3. 启动 Web Server: python -m fastchat.serve.gradio_web_server_multi")
        print()
        print("或者运行: ./start_chateval_arena.sh")
        return 0
    else:
        print()
        print("❌ 部分测试失败，请检查错误信息。")
        return 1

if __name__ == "__main__":
    sys.exit(main())

