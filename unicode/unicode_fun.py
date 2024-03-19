blocks_file = open('Blocks.txt','r')
count = 0

for line in blocks_file:
    if line[0] != '#' and len(line)> 1:
        ls = line.strip()
        [block,title] = ls.split(';')[0:2]
        block_numbers = block.split('..')
        start = int(f'0x{block_numbers[0]}',16)
        end = int(f'0x{block_numbers[1]}',16)
        #print(f'Line = {title} | Block = {block_numbers} |  Range = {start} - {end}')
        print(f'Starting on block {title}, which is the range {block_numbers}')
        outfile = open(f'output/{block_numbers[0]}_{block_numbers[1]}_{title.strip()}.txt','w')
        for i in range(start,end+1):
            try:
                print(f'Hex {hex(i)} || Decimal {i} || Character {chr(i)}')
                outfile.write(f'Hex {hex(i)} || Decimal {i} || Character {chr(i)} \n')
            except UnicodeEncodeError:
                pass
        outfile.close()

blocks_file.close()
