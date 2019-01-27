while [ true ]
do 
i2cdump -y 1 0x10
sleep 1
done
