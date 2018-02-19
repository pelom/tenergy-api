$(document).ready(function(){
    moment.locale('pt-BR');

    get_status_charge = function(status) {
        if(status.trim() == '00 No charging') {
            return 'Não carregando'
        } else if(status.trim() == '02 Boost') {
            return 'Carregando'
        } else if(status.trim() == '01 Float') {
            return 'Flutuando'
        }
        return status;
    }
    get_status_battery = function(status) {
        if(status.trim() == '00H Normal') {
            return 'Normal'
        }
        return status;
    }
    get_data = function() {
        $.get('http://localhost:5000/device/monitor', function(data) {
            console.log(data)
            $('#pvvoltage').text(data.pv.voltage)
            $('#pvcurrent').text(data.pv.current)
            $('#pvpower').text(data.pv.power)

            $('#pvvoltagemax').text(data.statistical.VoltageMaxPV)
            $('#pvvoltagemin').text(data.statistical.VoltageMinPV)

            $('#generatedenergy').text(data.statistical.GeneratedEnergy)

            $('#batteryvoltage').text(data.battery.voltage)
            $('#batterycurrent').text(data.battery.current)
            $('#batterypower').text(data.battery.power)

            $('#batterysoc').width( data.BatterySOC +'%');
            $('#batterysocvalue').text(data.BatterySOC + '%')

            $('#batterystatus').text(get_status_battery(data.StatusBattery))
            $('#batterycharge').text(get_status_charge(data.StatusCharge))

            $('#batterytemperature').text(data.temperature.Battery)
            $('#batterytemperatureremote').text(data.temperature.RemoteBattery)

            $('#batteryvoltagemax').text(data.statistical.VoltageMaxBattery)
            $('#batteryvoltagemin').text(data.statistical.VoltageMinBattery)

            $('#dischargingvoltage').text(data.discharging.voltage)
            $('#dischargingcurrent').text(data.discharging.current)
            $('#dischargingpower').text(data.discharging.power)
            $('#consumedenergy').text(data.statistical.ConsumedEnergy)

            $('#systemvoltage').text(data.VoltageSystemBattery)
            $('#temperatureinsideequipment').text(data.temperature.InsideEquipment)
            $('#temperaturepowercomponents').text(data.temperature.PowerComponents)
            $('#statusdischarging').text(data.StatusDischarging)

            $('#rtc').text(moment(data.rtc).format('LLLL'))
            $('#pvicon').removeClass('fa-sun fa-moon')
            $('#ctn_pv').removeClass('bg-light text-dark bg-dark text-white')
            if(data.StatusCharge.trim() == '00 No charging') {
                $('#ctn_pv').addClass('bg-light text-dark')
                $('#pvicon').addClass('fa-moon')
            } else {
                $('#ctn_pv').addClass('bg-warning text-dark')
                $('#pvicon').addClass('fa-sun')
            }
        });
    }
    window.setInterval(get_data, 2500);
});