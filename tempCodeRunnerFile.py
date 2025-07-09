            # Tách operands bởi dấu phẩy ngoài ngoặc vuông
            def split_operands(s):
                ops = []
                buf = ''
                bracket = 0
                for c in s:
                    if c == '[':
                        bracket += 1
                        buf += c
                    elif c == ']':
                        bracket -= 1
                        buf += c
                    elif c == ',' and bracket == 0:
                        if buf.strip():
                            ops.append(buf.strip())
                        buf = ''
                    else:
                        buf += c
                if buf.strip():
                    ops.append(buf.strip())
                return ops

            operands = split_operands(parts[1]) if len(parts) > 1 else []
