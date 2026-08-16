import urllib.request
import json

# 测试数据：20cm 手圈 + 金刚结 + 72号玉线
data = {
    'bracelet_length': 20,
    'knot_type': '金刚结',
    'thread_type': '72号玉线',
    'is_heart_snake': False
}

print("=" * 50)
print("测试编绳长度计算器 API")
print("=" * 50)
print(f"输入：{json.dumps(data, ensure_ascii=False, indent=2)}")
print("-" * 50)

try:
    req = urllib.request.Request(
        'http://127.0.0.1:8000/api/calculate',
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print("-" * 50)
        if result.get('success'):
            print("✅ 计算成功！")
            print(f"所需线长: {result['final_length']} cm")
            print(f"每条线长: {result['per_thread_length']} cm")
        else:
            print("❌ 计算失败")
            print(f"错误: {result.get('message')}")
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()
