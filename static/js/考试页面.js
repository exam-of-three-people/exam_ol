
function Submission_results() {
    subject=0;
    correct=0;
    for (item = 0; item < contents.length; i++) {
        subject = subject + 1;
        if (contents[i].question == contents[i].answer) {
            print('第%d道题回答正确', i - 1)
            correct = correct + 1;

        }
    }
    lv = correct / subject;
    alert('你的成绩为' + str(lv))
}
