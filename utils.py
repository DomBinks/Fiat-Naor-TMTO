def save_results(file, results):
    with open(file, 'a') as f:
        for i in range(len(results)):
            if 'a_found' in results[i]: # Fiat-Naor TMTO
                f.write(f""
                        f"{results[i]['size']},"
                        f"{results[i]['calls']},"
                        f"{results[i]['success_rate']:.{4}},"
                        f"{results[i]['time']:.{4}},"
                        f"{results[i]['a_found']:.{4}},"
                        f"{results[i]['t_found']:.{4}},"
                        f"{results[i]['function']},"
                        f"{results[i]['N']},"
                        f"{results[i]['t']},"
                        f"{results[i]['m']},"
                        f"{results[i]['l']},"
                        f"{results[i]['d']}"
                        #f"{results[i]['a_size']}"
                        f"\n")
            else: # Rainbow Tables
                f.write(f""
                        f"{results[i]['size']},"
                        f"{results[i]['calls']},"
                        f"{results[i]['success_rate']:.{4}},"
                        f"{results[i]['collisions']:.{4}},"
                        f"{results[i]['false_alarms']},"
                        f"{results[i]['time']:.{4}},"
                        f"{results[i]['function']},"
                        f"{results[i]['N']},"
                        f"{results[i]['t']},"
                        f"{results[i]['m']},"
                        f"{results[i]['l']}"
                        f"\n")
    f.close()

def open_results(file):
    results = []

    with open(file, 'r') as f:
        fields = f.readline().rstrip().split(',')
        int_fields = {'size', 'calls', 'calls_success', 'false_alarms', 'N', 'a_size'}
        float_fields = {'success_rate', 'collisions', 'time', 'a_found', 't_found', 't', 'm', 'l', 'd'}
        string_fields = {'function'}

        for line in f.readlines():
            parts = line.rstrip().split(',')

            result = {}
            for part in range(0,len(parts)):
                if fields[part] in int_fields:
                    result[fields[part]] = int(parts[part])
                elif fields[part] in float_fields:
                    result[fields[part]] = float(parts[part])
                elif fields[part] in string_fields:
                    result[fields[part]] = parts[part]

            results.append(result)
    f.close()

    return results