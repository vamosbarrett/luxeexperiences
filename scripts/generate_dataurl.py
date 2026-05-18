import sys, base64
if len(sys.argv)<3:
    print('Usage: generate_dataurl.py input.png out.txt')
    sys.exit(2)
inp=sys.argv[1]
out=sys.argv[2]
with open(inp,'rb') as f:
    b=base64.b64encode(f.read()).decode('ascii')
with open(out,'w',encoding='utf-8') as f:
    f.write('data:image/png;base64,'+b)
print('WROTE', out)
