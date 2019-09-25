import json

class Histogram():
    def __init__(self):
        self.__points = []
    def add(self, value, freq, is_anomaly):
        self.__points.append((value, freq, is_anomaly))
    def set_points(self, values, frequencies, is_anomaly):
        for i in range(len(values)):
            self.__points.append((values[i], frequencies[i], is_anomaly[i]))
    def to_dict(self):
        res = [{
            "value": x[0],
            "frequency": x[1],
            "anomaly": x[2]
        } for x in self.__points]
        return res

class ResultsGenerator():
    def __init__(self):
        self.__version = "0.0.1"
        self.__communications = []
    def add_communication(self, version, account, interface, src_ip, dst_ip, dst_port,
                          protocol, start_date, end_date, comm_hist, pack_hist, bytes_hist):
        self.__communications.append({
            "version":  version,
            "accountId": account,
            "interfaceId": interface,
            "srcIp": src_ip,
            "dstIp": dst_ip,
            "dstPort": dst_port,
            "protocol": protocol,
            "startDate": start_date,
            "endDate": end_date,
            "histograms": {
                "communicationDeltaTime": comm_hist.to_dict(),
                "packets": pack_hist.to_dict(),
                "bytes": bytes_hist.to_dict()
            }
        })
    def to_dict(self):
        return {
            "version": self.__version,
            "suspiciousCommunications": self.__communications
        }
    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)

if __name__ == "__main__":
    r = ResultsGenerator()
    comm_hist = Histogram()
    comm_hist.set_points([1,2,3],[100,10,3],[False, False, False])
    pack_hist = Histogram()
    bytes_hist = Histogram()
    r.add_communication("2", "1234", "123", "1.2.3.4", "4.3.2.1",
                        123, 6, "2018/12/20 13:40", "2018/12/21 10:37",
                        comm_hist, pack_hist, bytes_hist)
    print(r.to_json())