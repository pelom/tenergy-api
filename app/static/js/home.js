$(document).ready(function(){
    moment.locale('pt-BR');
    //moment.locale('en-US');

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
        } else if(status.trim() == '02H Under Volt') {
            return 'Tensão Inferior'
        } else if(status.trim() == '03H Low Volt Disconnect') {
            return 'Tensão Baixa - Disconectado'
        }

        return status;
    }
    get_data = function() {
        $.get(url_context + 'device/monitorredirect', function(datajson) {
            console.log(datajson)
            data = datajson.sample

            $('#pvpoweravg').text(datajson.generated.power.avg.toFixed(2))
            $('#pvpowermax').text(datajson.generated.power.max)
            $('#pvpowermin').text(datajson.generated.power.min)

            $('#pvvoltageavg').text(datajson.generated.voltage.avg.toFixed(2))
            $('#pvvoltagemax').text(datajson.generated.voltage.max)
            $('#pvvoltagemin').text(datajson.generated.voltage.min)

            $('#pvcurrentavg').text(datajson.generated.current.avg.toFixed(2))
            $('#pvcurrentmax').text(datajson.generated.current.max)
            $('#pvcurrentmin').text(datajson.generated.current.min)
            $('#pvcurrenttotal').text(datajson.generated.current.total.toFixed(2))

            $('#batterysoc').width( data.BatterySOC +'%');
            $('#batterysocvalue').text(data.BatterySOC + '%')

            $('#batterystatus').text(get_status_battery(data.StatusBattery))
            $('#batterycharge').text(get_status_charge(data.StatusCharge))

            $('#batterytemperature').text(data.temperature.Battery)
            $('#batterytemperatureremote').text(data.temperature.RemoteBattery)

            var toValue = function(value) {
                return !value ? 0 : value.toFixed(2)
            };
            $('#batterypoweravg').text(toValue(datajson.battery.power.avg))
            $('#batterypowermax').text(datajson.battery.power.max)
            $('#batterypowermin').text(datajson.battery.power.min)

            $('#batteryvoltageavg').text(toValue(datajson.battery.voltage.avg))
            $('#batteryvoltagemax').text(datajson.battery.voltage.max)
            $('#batteryvoltagemin').text(datajson.battery.voltage.min)

            $('#batterycurrentavg').text(toValue(datajson.battery.current.avg))
            $('#batterycurrentmax').text(datajson.battery.current.max)
            $('#batterycurrentmin').text(datajson.battery.current.min)

            $('#dischargingpoweravg').text(toValue(datajson.discharging.power.avg))
            $('#dischargingpowermax').text(datajson.discharging.power.max)
            $('#dischargingpowermin').text(datajson.discharging.power.min)

            $('#dischargingvoltageavg').text(toValue(datajson.discharging.voltage.avg))
            $('#dischargingvoltagemax').text(datajson.discharging.voltage.max)
            $('#dischargingvoltagemin').text(datajson.discharging.voltage.min)

            $('#dischargingcurrentavg').text(toValue(datajson.discharging.current.avg))
            $('#dischargingcurrentmax').text(datajson.discharging.current.max)
            $('#dischargingcurrentmin').text(datajson.discharging.current.min)

            $('#rtc').text(moment(data.CreatedDate).format('LLLL'))

            $('.pvicon').removeClass('fa-sun fa-moon')
            $('#ctn_pv').removeClass('bg-light text-dark bg-dark text-white')

            if(data.StatusCharge.trim() == '00 No charging') {
                $('#ctn_pv').addClass('bg-light text-dark')
                $('.pvicon').addClass('fa-moon')
            } else {
                $('#ctn_pv').addClass('bg-warning text-dark')
                $('.pvicon').addClass('fa-sun')
            }

            $('#headerstartdate').text(moment(datajson.generated.start).format('HH:mm'));
            $('#headerenddate').text(moment(datajson.generated.end).format('HH:mm'));

            $('#headerload').text(data.StatusDischarging)
            $('#headerbatterysystem').text(data.VoltageSystemBattery + 'V')
            $('#headerbatterystatus').text(get_status_battery(data.StatusBattery))
            $('#headerbatterycharge').text(get_status_charge(data.StatusCharge))

            gaugevolt.set(data.pv.voltage);
            gaugecurrent.set(data.pv.current);
            gaugepower.set(data.pv.power);
            gaugepowertotal.set(datajson.generated.power.total);

            gaugebatteryvolt.set(data.battery.voltage);
            gaugebatterycurrent.set(data.battery.current);
            gaugebatterypower.set(data.battery.power);
            gaugebatterysoc.set(data.BatterySOC);
            gaugetemperature.set(data.temperature.Battery);
            gaugeremote.set(data.temperature.RemoteBattery);

            gaugedischargingvolt.set(data.discharging.voltage);
            gaugedischargingcurrent.set(data.discharging.current);
            gaugedischargingpower.set(data.discharging.power);
            gaugedischargingpowertotal.set(datajson.discharging.power.total);

            gaugetemperatureinside.set(data.temperature.InsideEquipment);
            gaugetemperaturecomponent.set(data.temperature.PowerComponents);
        });
    }
    get_data()
    window.setInterval(get_data, 60000);

    var opts = {
        angle: -0.1, // The span of the gauge arc
        lineWidth: 0.2, // The line thickness
        radiusScale: 1, // Relative radius
        pointer: {
            length: 0.65, // // Relative to gauge radius
            strokeWidth: 0.055, // The thickness
            color: '#FFF' // Fill color
        },
        limitMax: false,     // If false, max value increases automatically if value > maxValue
        limitMin: false,     // If true, the min value of the gauge will be fixed
        colorStart: '#6FADCF',   // Colors
        colorStop: '#8FC0DA',    // just experiment with them
        strokeColor: '#E0E0E0',  // to see which ones work best for you
        generateGradient: true,
        highDpiSupport: true,     // High resolution support
        percentColors: [[0.0, "#ff0000" ], [0.50, "#f9c802"], [1.0, "#a9d70b"]],

        renderTicks: {
          divisions: 5,
          divWidth: 1.1,
          divLength: 0.7,
          divColor: "#333333",
          subDivisions: 3,
          subLength: 0.5,
          subWidth: 0.6,
          subColor: "#666666"
        },

//        staticZones: [
//           {strokeStyle: "#F03E3E", min: 0, max: 15  }, // Red from 100 to 130
//           {strokeStyle: "#FFDD00", min: 15, max: 30 }, // Yellow
//           {strokeStyle: "#30B32D", min: 30, max: 50 }, // Green
//        ],

//        staticLabels: {
//          font: "8px sans-serif",  // Specifies font
//          labels: [0, 15, 30, 5],  // Print labels at these values
//          color: "#000000",  // Optional: Label text color
//          fractionDigits: 0  // Optional: Numerical precision. 0=round off.
//        },
    };

//    var target = document.getElementById('canvas-preview'); // your canvas element
//    var gauge = new Gauge(target).setOptions(opts); // create sexy gauge!
//    gauge.setTextField(document.getElementById("preview-textfield"));

    var CustomTextRenderer = function(el) {
        this.el = el;
        this.render = function(gauge) {
            this.el.innerHTML = gauge.displayedValue.toFixed(2);
        }
    }
    CustomTextRenderer.prototype = new TextRenderer();

    var gaugevolt = new Gauge(document.getElementById("canvas-volt"));
    opts.staticZones= [
       {strokeStyle: "#F03E3E", min: 0, max: 15  },
       {strokeStyle: "#FFDD00", min: 15, max: 24 },
       {strokeStyle: "#30B32D", min: 24, max: 100 },
    ];
    gaugevolt.setOptions(opts);
    gaugevolt.setTextField(new CustomTextRenderer(document.getElementById("volt-textfield")))
    gaugevolt.maxValue = 100.0;
    gaugevolt.setMinValue(0.0);
    gaugevolt.animationSpeed = 32;

    opts.staticZones = [
       {strokeStyle: "#30B32D", min: 0, max: 5  }, // Red from 100 to 130
       {strokeStyle: "#FFDD00", min: 5, max: 15 }, // Yellow
       {strokeStyle: "#F03E3E", min: 15, max: 40 }, // Green
    ];
    var gaugecurrent = new Gauge(document.getElementById("canvas-current"));
    gaugecurrent.setOptions(opts);
    gaugecurrent.setTextField(new CustomTextRenderer(document.getElementById("current-textfield")))
    gaugecurrent.maxValue = 40.0;
    gaugecurrent.setMinValue(0.0);
    gaugecurrent.animationSpeed = 32;

    opts.staticZones = undefined;
    var gaugepower = new Gauge(document.getElementById("canvas-power"));
    gaugepower.setOptions(opts);
    gaugepower.setTextField(new CustomTextRenderer(document.getElementById("power-textfield")))
    gaugepower.maxValue = 1040.0;
    gaugepower.setMinValue(0.0);
    gaugepower.animationSpeed = 32;

    opts.staticZones = undefined;
    var gaugepowertotal = new Gauge(document.getElementById("canvas-powertotal"));
    gaugepowertotal.setOptions(opts);
    gaugepowertotal.setTextField(new CustomTextRenderer(document.getElementById("powertotal-textfield")))
    gaugepowertotal.maxValue = 5000.0;
    gaugepowertotal.setMinValue(0.0);
    gaugepowertotal.animationSpeed = 32;

    opts.staticZones = [
       {strokeStyle: "#F03E3E", min: 9, max: 21.2  }, // Red from 100 to 130
       {strokeStyle: "#FFDD00", min: 21.2, max: 25.2 }, // Yellow
       {strokeStyle: "#30B32D", min: 25.2, max: 30 }, // Green
       {strokeStyle: "#F03E3E", min: 30, max: 36 }, // Green
    ];
    var gaugebatteryvolt = new Gauge(document.getElementById("canvas-batteryvolt"));
    gaugebatteryvolt.setOptions(opts);
    gaugebatteryvolt.setTextField(new CustomTextRenderer(document.getElementById("batteryvolt-textfield")))
    gaugebatteryvolt.maxValue = 36.0;
    gaugebatteryvolt.setMinValue(9);
    gaugebatteryvolt.animationSpeed = 32;

    opts.staticZones = [
       {strokeStyle: "#30B32D", min: 0, max: 5  }, // Red from 100 to 130
       {strokeStyle: "#FFDD00", min: 5, max: 15 }, // Yellow
       {strokeStyle: "#F03E3E", min: 15, max: 40 }, // Green
    ];
    var gaugebatterycurrent = new Gauge(document.getElementById("canvas-batterycurrent"));
    gaugebatterycurrent.setOptions(opts);
    gaugebatterycurrent.setTextField(new CustomTextRenderer(document.getElementById("batterycurrent-textfield")))
    gaugebatterycurrent.maxValue = 40.0;
    gaugebatterycurrent.setMinValue(0.0);
    gaugebatterycurrent.animationSpeed = 32;

    opts.staticZones = undefined;
    var gaugebatterypower = new Gauge(document.getElementById("canvas-batterypower"));
    gaugebatterypower.setOptions(opts);
    gaugebatterypower.setTextField(new CustomTextRenderer(document.getElementById("batterypower-textfield")))
    gaugebatterypower.maxValue = 1000.0;
    gaugebatterypower.setMinValue(0.0);
    gaugebatterypower.animationSpeed = 32;

    opts.staticZones = [
       {strokeStyle: "#F03E3E", min: 0, max: 33  }, // Red from 100 to 130
       {strokeStyle: "#FFDD00", min: 33, max: 66 }, // Yellow
       {strokeStyle: "#30B32D", min: 66, max: 100 }, // Green
    ];
    var gaugebatterysoc = new Gauge(document.getElementById("canvas-batterysoc"));
    gaugebatterysoc.setOptions(opts);
    gaugebatterysoc.setTextField(document.getElementById("batterysoc-textfield"))
    gaugebatterysoc.maxValue = 100.0;
    gaugebatterysoc.setMinValue(0.0);
    gaugebatterysoc.animationSpeed = 32;

    opts.staticZones = [
       { strokeStyle: "#EEEEE", min: 0, max: 25  }, // Red from 100 to 130
       { strokeStyle: "#FFDD00", min: 25, max: 45 }, // Yellow
       { strokeStyle: "#F03E3E", min: 45, max: 60 }, // Green
    ];
    var gaugetemperature = new Gauge(document.getElementById("canvas-temperature"));
    gaugetemperature.setOptions(opts);
    gaugetemperature.setTextField(document.getElementById("temperature-textfield"))
    gaugetemperature.maxValue = 60.0;
    gaugetemperature.setMinValue(0.0);
    gaugetemperature.animationSpeed = 32;

    opts.staticZones = [
       { strokeStyle: "#EEEEE", min: 0, max: 25  }, // Red from 100 to 130
       { strokeStyle: "#FFDD00", min: 25, max: 45 }, // Yellow
       { strokeStyle: "#F03E3E", min: 45, max: 60 }, // Green
    ];
    var gaugeremote = new Gauge(document.getElementById("canvas-remote"));
    gaugeremote.setOptions(opts);
    gaugeremote.setTextField(new CustomTextRenderer(document.getElementById("remote-textfield")))
    gaugeremote.maxValue = 60.0;
    gaugeremote.setMinValue(0.0);
    gaugeremote.animationSpeed = 32;


    opts.staticZones = [
       { strokeStyle: "#EEEEE", min: 0, max: 25  }, // Red from 100 to 130
       { strokeStyle: "#FFDD00", min: 25, max: 45 }, // Yellow
       { strokeStyle: "#F03E3E", min: 45, max: 60 }, // Green
    ];
    var gaugetemperatureinside = new Gauge(document.getElementById("canvas-inside"));
    gaugetemperatureinside.setOptions(opts);
    gaugetemperatureinside.setTextField(new CustomTextRenderer(document.getElementById("inside-textfield")))
    gaugetemperatureinside.maxValue = 60.0;
    gaugetemperatureinside.setMinValue(0.0);
    gaugetemperatureinside.animationSpeed = 32;

    opts.staticZones = [
       { strokeStyle: "#EEEEE", min: 0, max: 25  }, // Red from 100 to 130
       { strokeStyle: "#FFDD00", min: 25, max: 45 }, // Yellow
       { strokeStyle: "#F03E3E", min: 45, max: 60 }, // Green
    ];
    var gaugetemperaturecomponent = new Gauge(document.getElementById("canvas-component"));
    gaugetemperaturecomponent.setOptions(opts);
    gaugetemperaturecomponent.setTextField(new CustomTextRenderer(document.getElementById("component-textfield")))
    gaugetemperaturecomponent.maxValue = 60.0;
    gaugetemperaturecomponent.setMinValue(0.0);
    gaugetemperaturecomponent.animationSpeed = 32;

    var gaugedischargingvolt = new Gauge(document.getElementById("canvas-dischargingvolt"));
   opts.staticZones = [
       {strokeStyle: "#F03E3E", min: 9, max: 21.2  }, // Red from 100 to 130
       {strokeStyle: "#FFDD00", min: 21.2, max: 25.2 }, // Yellow
       {strokeStyle: "#30B32D", min: 25.2, max: 30 }, // Green
       {strokeStyle: "#F03E3E", min: 30, max: 36 }, // Green
    ];
    gaugedischargingvolt.setOptions(opts);
    gaugedischargingvolt.setTextField(new CustomTextRenderer(document.getElementById("dischargingvolt-textfield")))
    gaugedischargingvolt.maxValue = 36.0;
    gaugedischargingvolt.setMinValue(9.0);
    gaugedischargingvolt.animationSpeed = 32;

    opts.staticZones = [
       {strokeStyle: "#30B32D", min: 0, max: 5  }, // Red from 100 to 130
       {strokeStyle: "#FFDD00", min: 5, max: 15 }, // Yellow
       {strokeStyle: "#F03E3E", min: 15, max: 40 }, // Green
    ];
    var gaugedischargingcurrent = new Gauge(document.getElementById("canvas-dischargingcurrent"));
    gaugedischargingcurrent.setOptions(opts);
    gaugedischargingcurrent.setTextField(new CustomTextRenderer(document.getElementById("dischargingcurrent-textfield")))
    gaugedischargingcurrent.maxValue = 40.0;
    gaugedischargingcurrent.setMinValue(0.0);
    gaugedischargingcurrent.animationSpeed = 32;

    opts.staticZones = undefined;
    var gaugedischargingpower = new Gauge(document.getElementById("canvas-dischargingpower"));
    gaugedischargingpower.setOptions(opts);
    gaugedischargingpower.setTextField(new CustomTextRenderer(document.getElementById("dischargingpower-textfield")))
    gaugedischargingpower.maxValue = 1000.0;
    gaugedischargingpower.setMinValue(0.0);
    gaugedischargingpower.animationSpeed = 32;

    opts.staticZones = undefined;
    var gaugedischargingpowertotal = new Gauge(document.getElementById("canvas-dischargingpowertotal"));
    gaugedischargingpowertotal.setOptions(opts);
    gaugedischargingpowertotal.setTextField(new CustomTextRenderer(document.getElementById("dischargingpowertotal-textfield")))
    gaugedischargingpowertotal.maxValue = 5000.0;
    gaugedischargingpowertotal.setMinValue(0.0);
    gaugedischargingpowertotal.animationSpeed = 32;

    $.get(url_context + 'device/grouphourredirect', function(datajson) {
        console.log(datajson)

        labels = []
        tensao = []
        corrente = []
        potencia = []
        soc = []
        datajson.forEach(function (item) {
          labels.splice(0, 0, parseInt(new Date(item.CreatedDate).getHours()));
          tensao.splice(0, 0, item.VoltageBattery)
          corrente.splice(0, 0, item.CurrentBattery);
          potencia.splice(0, 0, item.PowerBattery);
          soc.splice(0, 0, item.BatterySOC);
        })

        Chart.defaults.global.defaultFontColor = '#FFF';
        new Chart(document.getElementById("myChart"), {
          type: 'line',
          data: {
            labels: labels,
            datasets: [{
                data: tensao,
                label: "Tensão",
                borderColor: "#3e95cd",
                fill: false
              }, {
                data: corrente,
                label: "Corrente",
                borderColor: "#8e5ea2",
                fill: false
              }, {
                data: potencia,
                label: "Potência",
                borderColor: "#3cba9f",
                fill: false
              }, {
                data: soc,
                label: "SOC",
                borderColor: "#e8c3b9",
                fill: false
              }
            ]
          },
          options: {
            title: {
              display: true,
              text: 'Média por hora'
            },
            /*tooltips: {
              mode: 'label',
            },*/
            hover: {
              mode: 'nearest',
              intersect: true
            },
            scales: {
              xAxes: [{
                display: true,
                gridLines: {
                  display: true,
                  /*color: "#EEE"*/
                },
                scaleLabel: {
                  display: true,
                  labelString: 'Hora'
                }
              }],
              yAxes: [{
                display: true,
                gridLines: {
                  display: true
                },
                scaleLabel: {
                  display: true,
                  labelString: 'Média'
                }
              }]
            }
          }
        });
    })

});